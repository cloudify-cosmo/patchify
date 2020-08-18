diff --git a/cloudify/amqp_client.py b/cloudify/amqp_client.py
index da630f8..d21df27 100644
--- a/cloudify/amqp_client.py
+++ b/cloudify/amqp_client.py
@@ -466,8 +466,15 @@ class SendHandler(object):
         level = message.get('level', 'info')
         log_func = getattr(self.logger, level, self.logger.info)
         exec_id = message.get('context', {}).get('execution_id')
+        execution_creator_username = message.get('context', {}).get(
+            'execution_creator_username')
         text = message['message']['text']
-        msg = u'[{0}] {1}'.format(exec_id, text) if exec_id else text
+        if exec_id:
+            msg = u'[{0}] {1}'.format(exec_id, text)
+            if execution_creator_username:
+                msg = u'[{0}] '.format(execution_creator_username) + msg
+        else:
+            msg = text
         log_func(msg)
 
     def publish(self, message, **kwargs):
