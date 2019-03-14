diff --git a/cloudify/amqp_client.py b/cloudify/amqp_client.py
index 600d2d6..61e7c2b 100644
--- a/cloudify/amqp_client.py
+++ b/cloudify/amqp_client.py
@@ -22,6 +22,7 @@ import uuid
 import Queue
 import logging
 import threading
+from collections import deque
 from urlparse import urlsplit, urlunsplit
 
 import pika
@@ -124,7 +125,6 @@ class AMQPConnection(object):
     def __init__(self, handlers, name=None, amqp_params=None,
                  connect_timeout=10):
         self._handlers = handlers
-        self._publish_queue = Queue.Queue()
         self.name = name
         self._connection_params = self._get_connection_params()
         self._reconnect_backoff = 1
@@ -137,6 +137,12 @@ class AMQPConnection(object):
         self._error = None
         self._daemon_factory = _get_daemon_factory()
 
+        # use this queue to schedule methods to be called on the pika channel
+        # from the connection thread - for sending data to rabbitmq, eg.
+        # publishing messages or sending ACKs, which needs to be done from
+        # the connection thread
+        self._connection_tasks_queue = Queue.Queue()
+
     @staticmethod
     def _update_env_vars(new_host):
         """
@@ -265,23 +271,25 @@ class AMQPConnection(object):
     def _process_publish(self, channel):
         while True:
             try:
-                envelope = self._publish_queue.get_nowait()
+                envelope = self._connection_tasks_queue.get_nowait()
             except Queue.Empty:
                 return
 
+            target_channel = envelope['channel'] or channel
+            method = envelope['method']
             # we use a separate queue to send any possible exceptions back
             # to the calling thread - see the publish method
             message = envelope['message']
             err_queue = envelope.get('err_queue')
 
             try:
-                channel.publish(**message)
+                getattr(target_channel, method)(**message)
             except pika.exceptions.ConnectionClosed:
                 if self._closed:
                     return
                 # if we couldn't send the message because the connection
                 # was down, requeue it to be sent again later
-                self._publish_queue.put(envelope)
+                self._connection_tasks_queue.put(envelope)
                 raise
             except Exception as e:
                 if err_queue:
@@ -308,16 +316,12 @@ class AMQPConnection(object):
                 'Attempted to open a channel on a closed connection')
         return self._pika_connection.channel()
 
-    def publish(self, message, wait=True, timeout=None):
-        """Schedule a message to be sent.
+    def channel_method(self, method, channel=None, wait=True,
+                       timeout=None, **kwargs):
+        """Schedule a channel method to be called from the connection thread.
 
-        :param message: Kwargs for the pika basic_publish call. Should at
-                        least contain the "body" and "exchange" keys, and
-                        it might contain other keys such as "routing_key"
-                        or "properties"
-        :param wait: Whether to wait for the message to actually be sent.
-                     If true, an exception will be raised if the message
-                     cannot be sent.
+        Use this to schedule a channel method such as .publish or .basic_ack
+        to be called from the connection thread.
         """
         if wait and self._consumer_thread \
                 and self._consumer_thread is threading.current_thread():
@@ -333,15 +337,34 @@ class AMQPConnection(object):
         # contain either an exception instance, or None
         err_queue = Queue.Queue() if wait else None
         envelope = {
-            'message': message,
-            'err_queue': err_queue
+            'method': method,
+            'message': kwargs,
+            'err_queue': err_queue,
+            'channel': channel
         }
-        self._publish_queue.put(envelope)
+        self._connection_tasks_queue.put(envelope)
         if err_queue:
             err = err_queue.get(timeout=timeout)
             if isinstance(err, Exception):
                 raise err
 
+    def publish(self, message, wait=True, timeout=None):
+        """Schedule a message to be sent.
+
+        :param message: Kwargs for the pika basic_publish call. Should at
+                        least contain the "body" and "exchange" keys, and
+                        it might contain other keys such as "routing_key"
+                        or "properties"
+        :param wait: Whether to wait for the message to actually be sent.
+                     If true, an exception will be raised if the message
+                     cannot be sent.
+        """
+        self.channel_method('publish', wait=wait, timeout=timeout, **message)
+
+    def ack(self, channel, delivery_tag, wait=True, timeout=None):
+        self.channel_method('basic_ack', wait=wait, timeout=timeout,
+                            channel=channel, delivery_tag=delivery_tag)
+
 
 class TaskConsumer(object):
     routing_key = ''
@@ -415,10 +438,13 @@ class TaskConsumer(object):
         raise NotImplementedError()
 
     def delete_queue(self, queue):
-        self.in_channel.queue_delete(queue, if_empty=True)
+        self._connection.channel_method(
+            'queue_delete', queue=queue, channel=self.in_channel,
+            if_empty=True)
 
     def delete_exchange(self, exchange):
-        self.in_channel.exchange_delete(exchange)
+        self._connection.channel_method(
+            'exchange_delete', exchange=exchange, channel=self.in_channel)
 
 
 class SendHandler(object):
