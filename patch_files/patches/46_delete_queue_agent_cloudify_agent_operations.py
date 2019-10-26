diff --git a/cloudify_agent/operations.py b/cloudify_agent/operations.py
index d563e5e..c43e9ce 100644
--- a/cloudify_agent/operations.py
+++ b/cloudify_agent/operations.py
@@ -358,8 +358,7 @@ def _send_amqp_task(agent, params, timeout):
         raise RecoverableError('Agent is not responding')
 
     task = {'cloudify_task': {'kwargs': params}}
-    handler = amqp_client.BlockingRequestResponseHandler(
-        exchange=agent['queue'])
+    handler = amqp_client.BlockingRequestResponseHandler(agent['queue'])
 
     with _get_amqp_client(agent) as client:
         client.add_handler(handler)
