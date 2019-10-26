diff --git a/cloudify/amqp_client.py b/cloudify/amqp_client.py
index 7c4e449..a436be1 100644
--- a/cloudify/amqp_client.py
+++ b/cloudify/amqp_client.py
@@ -210,7 +210,7 @@ class AMQPConnection(object):
         out_channel = self._pika_connection.channel()
         out_channel.confirm_delivery()
         for handler in self._handlers:
-            handler.register(self)
+            handler.register(self, out_channel)
             logger.info('Registered handler for {0} [{1}]'
                         .format(handler.__class__.__name__,
                                 handler.routing_key))
@@ -282,7 +282,10 @@ class AMQPConnection(object):
             err_queue = envelope.get('err_queue')
 
             try:
-                getattr(target_channel, method)(**message)
+                if callable(method):
+                    method(self, channel, **message)
+                else:
+                    getattr(target_channel, method)(**message)
             except pika.exceptions.ConnectionClosed:
                 if self._closed:
                     return
@@ -307,7 +310,7 @@ class AMQPConnection(object):
     def add_handler(self, handler):
         self._handlers.append(handler)
         if self._pika_connection:
-            handler.register(self)
+            self.channel_method(handler.register)
 
     def channel(self):
         if self._closed or not self._pika_connection:
@@ -374,15 +377,10 @@ class TaskConsumer(object):
         self.queue = '{0}_{1}'.format(queue, self.routing_key)
         self._sem = threading.Semaphore(threadpool_size)
         self._connection = None
-        self.in_channel = None
         self.exchange_type = exchange_type
 
-    def register(self, connection):
+    def register(self, connection, channel):
         self._connection = connection
-        self.in_channel = connection.channel()
-        self._register_queue(self.in_channel)
-
-    def _register_queue(self, channel):
         channel.basic_qos(prefetch_count=self.threadpool_size)
         channel.confirm_delivery()
         channel.exchange_declare(exchange=self.exchange,
@@ -436,14 +434,12 @@ class TaskConsumer(object):
     def handle_task(self, full_task):
         raise NotImplementedError()
 
-    def delete_queue(self, queue):
+    def delete_queue(self, queue, if_empty=True, wait=True):
         self._connection.channel_method(
-            'queue_delete', queue=queue, channel=self.in_channel,
-            if_empty=True)
+            'queue_delete', queue=queue, if_empty=True, wait=wait)
 
     def delete_exchange(self, exchange):
-        self._connection.channel_method(
-            'exchange_delete', exchange=exchange, channel=self.in_channel)
+        self._connection.channel_method('exchange_delete', exchange=exchange)
 
 
 class SendHandler(object):
@@ -460,12 +456,11 @@ class SendHandler(object):
         self.logger = logging.getLogger('dispatch.{0}'.format(self.exchange))
         self._connection = None
 
-    def register(self, connection):
+    def register(self, connection, channel):
         self._connection = connection
-        out_channel = connection.channel()
-        out_channel.exchange_declare(exchange=self.exchange,
-                                     exchange_type=self.exchange_type,
-                                     **self.exchange_settings)
+        channel.exchange_declare(exchange=self.exchange,
+                                 exchange_type=self.exchange_type,
+                                 **self.exchange_settings)
 
     def _log_message(self, message):
         level = message.get('level', 'info')
@@ -490,7 +485,6 @@ class ScheduledExecutionHandler(SendHandler):
 
     def __init__(self, exchange, exchange_type, routing_key,
                  target_exchange, target_routing_key, ttl):
-
         super(ScheduledExecutionHandler, self).__init__(exchange,
                                                         exchange_type,
                                                         routing_key)
@@ -500,25 +494,26 @@ class ScheduledExecutionHandler(SendHandler):
         self.target_routing_key = target_routing_key
         self.ttl = ttl
 
-    def register(self, connection):
+    def register(self, connection, channel):
         self._connection = connection
-
-        out_channel = connection.channel()
-        out_channel.exchange_declare(exchange=self.exchange,
-                                     exchange_type=self.exchange_type,
-                                     **self.exchange_settings)
+        channel.exchange_declare(exchange=self.exchange,
+                                 exchange_type=self.exchange_type,
+                                 **self.exchange_settings)
         # Declare a new temporary queue for the Dead Letter Exchange, and
         # set the routing key of the MGMTWORKER queue
-        out_channel.queue_declare(queue=self.routing_key,
-                                  arguments={
-                                      'x-message-ttl': self.ttl,
-                                      'x-dead-letter-exchange':
-                                          self.target_exchange,
-                                      'x-dead-letter-routing-key':
-                                          self.target_routing_key
-                                  },
-                                  durable=True)
-        out_channel.queue_bind(exchange=self.exchange, queue=self.routing_key)
+        channel.queue_declare(
+            queue=self.routing_key,
+            arguments={
+                'x-message-ttl': self.ttl,
+                'x-dead-letter-exchange': (
+                    self.target_exchange
+                ),
+                'x-dead-letter-routing-key': (
+                    self.target_routing_key
+                ),
+            },
+            durable=True)
+        channel.queue_bind(exchange=self.exchange, queue=self.routing_key)
 
 
 class NoWaitSendHandler(SendHandler):
@@ -530,20 +525,23 @@ class NoWaitSendHandler(SendHandler):
 
 
 class _RequestResponseHandlerBase(TaskConsumer):
-    def __init__(self, exchange, queue=None):
-        super(_RequestResponseHandlerBase, self).__init__(exchange)
-        self.queue = queue or '{0}_response_{1}'.format(
-            self.exchange, uuid.uuid4().hex)
-
-    def _register_queue(self, channel):
-        self.in_channel.exchange_declare(exchange=self.exchange,
-                                         auto_delete=False,
-                                         durable=True,
-                                         exchange_type=self.exchange_type)
-        self.in_channel.queue_declare(queue=self.queue,
-                                      durable=True)
-        self.in_channel.queue_bind(queue=self.queue, exchange=self.exchange)
-        channel.basic_consume(self.process, self.queue)
+    queue_exclusive = False
+
+    def register(self, connection, channel):
+        self._connection = connection
+        channel.exchange_declare(exchange=self.exchange,
+                                 auto_delete=False,
+                                 durable=True,
+                                 exchange_type=self.exchange_type)
+
+    def _declare_queue(self, queue_name):
+        self._connection.channel_method(
+            'queue_declare', queue=queue_name, durable=True,
+            exclusive=self.queue_exclusive)
+        self._connection.channel_method(
+            'queue_bind', queue=queue_name, exchange=self.exchange)
+        self._connection.channel_method(
+            'basic_consume', queue=queue_name, consumer_callback=self.process)
 
     def publish(self, message, correlation_id, routing_key='',
                 expiration=None):
@@ -554,7 +552,7 @@ class _RequestResponseHandlerBase(TaskConsumer):
             'exchange': self.exchange,
             'body': json.dumps(message),
             'properties': pika.BasicProperties(
-                reply_to=self.queue,
+                reply_to=correlation_id,
                 correlation_id=correlation_id,
                 expiration=expiration),
             'routing_key': routing_key
@@ -565,37 +563,38 @@ class _RequestResponseHandlerBase(TaskConsumer):
 
 
 class BlockingRequestResponseHandler(_RequestResponseHandlerBase):
+    # when the process closes, a blockin handler's queues can be deleted,
+    # because there's no way to resume waiting on those
+    queue_exclusive = True
+
     def __init__(self, *args, **kwargs):
         super(BlockingRequestResponseHandler, self).__init__(*args, **kwargs)
-        self._response_queues = {}
+        self._response = Queue.Queue()
 
     def publish(self, message, *args, **kwargs):
         timeout = kwargs.pop('timeout', None)
         correlation_id = kwargs.pop('correlation_id', None)
         if correlation_id is None:
             correlation_id = uuid.uuid4().hex
-        self._response_queues[correlation_id] = Queue.Queue()
+
+        self._declare_queue(correlation_id)
         super(BlockingRequestResponseHandler, self).publish(
             message, correlation_id, *args, **kwargs)
+
         try:
-            resp = self._response_queues[correlation_id].get(timeout=timeout)
-            return resp
+            return json.loads(self._response.get(timeout=timeout))
         except Queue.Empty:
             raise RuntimeError('No response received for task {0}'
                                .format(correlation_id))
-        finally:
-            self.delete_queue(self.queue)
-            del self._response_queues[correlation_id]
+        except ValueError:
+            logger.error('Error parsing response for task {0}'
+                         .format(correlation_id))
 
     def process(self, channel, method, properties, body):
         channel.basic_ack(method.delivery_tag)
-        try:
-            response = json.loads(body)
-        except ValueError:
-            logger.error('Error parsing response: {0}'.format(body))
-            return
-        if properties.correlation_id in self._response_queues:
-            self._response_queues[properties.correlation_id].put(response)
+        self.delete_queue(
+            properties.correlation_id, wait=False, if_empty=False)
+        self._response.put(body)
 
 
 class CallbackRequestResponseHandler(_RequestResponseHandlerBase):
@@ -608,8 +607,10 @@ class CallbackRequestResponseHandler(_RequestResponseHandlerBase):
         correlation_id = kwargs.pop('correlation_id', None)
         if correlation_id is None:
             correlation_id = uuid.uuid4().hex
+
         if callback:
             self.wait_for_response(correlation_id, callback)
+        self._declare_queue(correlation_id)
         super(CallbackRequestResponseHandler, self).publish(
             message, correlation_id, *args, **kwargs)
 
@@ -618,14 +619,15 @@ class CallbackRequestResponseHandler(_RequestResponseHandlerBase):
 
     def process(self, channel, method, properties, body):
         channel.basic_ack(method.delivery_tag)
+        self.delete_queue(
+            properties.correlation_id, wait=False, if_empty=False)
+        if properties.correlation_id not in self._callbacks:
+            return
         try:
             response = json.loads(body)
+            self._callbacks[properties.correlation_id](response)
         except ValueError:
             logger.error('Error parsing response: {0}'.format(body))
-            return
-        if properties.correlation_id in self._callbacks:
-            channel.queue_delete(self.queue)
-            self._callbacks[properties.correlation_id](response)
 
 
 def get_client(amqp_host=None,
