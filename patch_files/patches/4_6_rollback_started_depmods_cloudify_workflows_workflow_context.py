diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 6c54967..4c2c536 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -57,6 +57,7 @@ from cloudify.logs import (CloudifyWorkflowLoggingHandler,
                            init_cloudify_logger,
                            send_workflow_event,
                            send_sys_wide_wf_event)
+from cloudify.models_states import DeploymentModificationState
 
 from cloudify.utils import is_agent_alive
 
@@ -1205,6 +1206,9 @@ class CloudifyWorkflowContextHandler(object):
     def rollback_deployment_modification(self, modification):
         raise NotImplementedError('Implemented by subclasses')
 
+    def list_deployment_modifications(self, status):
+        raise NotImplementedError('Implemented by subclasses')
+
     def scaling_groups(self):
         raise NotImplementedError('Implemented by subclasses')
 
@@ -1508,6 +1512,14 @@ class RemoteCloudifyWorkflowContextHandler(RemoteContextHandler):
         client = get_rest_client()
         client.deployment_modifications.rollback(modification.id)
 
+    def list_deployment_modifications(self, status):
+        deployment_id = self.workflow_ctx.deployment.id
+        client = get_rest_client()
+        modifications = client.deployment_modifications.list(
+            deployment_id=deployment_id,
+            status=status)
+        return [Modification(self.workflow_ctx, m) for m in modifications]
+
     def send_workflow_event(self, event_type, message=None, args=None,
                             additional_context=None):
         send_workflow_event(self.workflow_ctx,
@@ -1690,6 +1702,16 @@ class WorkflowDeploymentContext(context.DeploymentContext):
         handler = self.workflow_ctx.internal.handler
         return handler.start_deployment_modification(nodes)
 
+    def list_started_modifications(self):
+        """List modifications already started (and not finished)
+
+        :return: A list of workflow modification wrappers
+        :rtype: list of Modification
+        """
+        handler = self.workflow_ctx.internal.handler
+        return handler.list_deployment_modifications(
+            DeploymentModificationState.STARTED)
+
     @property
     def scaling_groups(self):
         return self.workflow_ctx.internal.handler.scaling_groups
