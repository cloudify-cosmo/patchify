diff --git a/cloudify_agent/tests/api/pm/__init__.py b/cloudify_agent/tests/api/pm/__init__.py
index 0d22ebe..8e6b7d9 100644
--- a/cloudify_agent/tests/api/pm/__init__.py
+++ b/cloudify_agent/tests/api/pm/__init__.py
@@ -434,7 +434,7 @@ class BaseDaemonProcessManagementTest(BaseDaemonLiveTestCase):
                                                  deployment_id=deployment_id)
         kwargs = kwargs or {}
         kwargs['__cloudify_context'] = cloudify_context
-        handler = amqp_client.BlockingRequestResponseHandler(exchange=queue)
+        handler = amqp_client.BlockingRequestResponseHandler(queue)
         client = amqp_client.get_client()
         client.add_handler(handler)
         with client:
