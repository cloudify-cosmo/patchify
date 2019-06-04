diff --git a/cloudify/amqp_client.py b/cloudify/amqp_client.py
index 61e7c2b..7c4e449 100644
--- a/cloudify/amqp_client.py
+++ b/cloudify/amqp_client.py
@@ -22,7 +22,6 @@ import uuid
 import Queue
 import logging
 import threading
-from collections import deque
 from urlparse import urlsplit, urlunsplit
 
 import pika
@@ -541,7 +540,7 @@ class _RequestResponseHandlerBase(TaskConsumer):
                                          auto_delete=False,
                                          durable=True,
                                          exchange_type=self.exchange_type)
-        self.in_channel.queue_declare(queue=self.queue, exclusive=True,
+        self.in_channel.queue_declare(queue=self.queue,
                                       durable=True)
         self.in_channel.queue_bind(queue=self.queue, exchange=self.exchange)
         channel.basic_consume(self.process, self.queue)
@@ -585,6 +584,7 @@ class BlockingRequestResponseHandler(_RequestResponseHandlerBase):
             raise RuntimeError('No response received for task {0}'
                                .format(correlation_id))
         finally:
+            self.delete_queue(self.queue)
             del self._response_queues[correlation_id]
 
     def process(self, channel, method, properties, body):
@@ -624,6 +624,7 @@ class CallbackRequestResponseHandler(_RequestResponseHandlerBase):
             logger.error('Error parsing response: {0}'.format(body))
             return
         if properties.correlation_id in self._callbacks:
+            channel.queue_delete(self.queue)
             self._callbacks[properties.correlation_id](response)
 
 
