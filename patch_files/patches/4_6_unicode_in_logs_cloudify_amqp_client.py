diff --git a/cloudify/amqp_client.py b/cloudify/amqp_client.py
index a436be1..da630f8 100644
--- a/cloudify/amqp_client.py
+++ b/cloudify/amqp_client.py
@@ -467,7 +467,7 @@ class SendHandler(object):
         log_func = getattr(self.logger, level, self.logger.info)
         exec_id = message.get('context', {}).get('execution_id')
         text = message['message']['text']
-        msg = '[{0}] {1}'.format(exec_id, text) if exec_id else text
+        msg = u'[{0}] {1}'.format(exec_id, text) if exec_id else text
         log_func(msg)
 
     def publish(self, message, **kwargs):
