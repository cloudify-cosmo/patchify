diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 4c2c536..6afdd5d 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -532,6 +532,10 @@ class _WorkflowContextBase(object):
         """Cloudify tenant"""
         return self._context.get('tenant', {})
 
+    @property
+    def execution_creator_username(self):
+        return self._context.get('execution_creator_username')
+
     def _init_cloudify_logger(self):
         logger_name = self.execution_id
         logging_handler = self.internal.handler.get_context_logging_handler()
@@ -1416,7 +1420,9 @@ class RemoteContextHandler(CloudifyWorkflowContextHandler):
     def operation_cloudify_context(self):
         return {'local': False,
                 'bypass_maintenance': utils.get_is_bypass_maintenance(),
-                'rest_token': utils.get_rest_token()}
+                'rest_token': utils.get_rest_token(),
+                'execution_creator_username':
+                    utils.get_execution_creator_username()}
 
     def download_deployment_resource(self,
                                      blueprint_id,
