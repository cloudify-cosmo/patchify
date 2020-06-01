diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 276f498..6ab0e79 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -1672,7 +1672,9 @@ class WorkflowDeploymentContext(context.DeploymentContext):
         :rtype: Modification
         """
         handler = self.workflow_ctx.internal.handler
-        return handler.start_deployment_modification(nodes)
+        modification = handler.start_deployment_modification(nodes)
+        self.workflow_ctx.refresh_node_instances()
+        return modification
 
     @property
     def scaling_groups(self):
