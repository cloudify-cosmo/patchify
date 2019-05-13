diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index ce63fbf..af9adf9 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -904,6 +904,21 @@ class WorkflowNodesAndInstancesContainer(object):
         """
         return self._node_instances.get(node_instance_id)
 
+    def refresh_node_instances(self):
+        if self.local:
+            storage = self.internal.handler.storage
+            raw_node_instances = storage.get_node_instances()
+        else:
+            rest = get_rest_client()
+            raw_node_instances = rest.node_instances.list(
+                deployment_id=self.deployment.id,
+                _get_all_results=True)
+        self._node_instances = dict(
+            (instance.id, CloudifyWorkflowNodeInstance(
+                self, self._nodes[instance.node_id], instance,
+                self))
+            for instance in raw_node_instances)
+
 
 class CloudifyWorkflowContext(
     _WorkflowContextBase,
