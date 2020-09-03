diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 6afdd5d..b793d82 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -1440,8 +1440,16 @@ class RemoteContextHandler(CloudifyWorkflowContextHandler):
 
     def get_operations(self, graph_id):
         client = get_rest_client()
-        operations = client.operations.list(graph_id)
-        return operations
+        ops = []
+        offset = 0
+        while True:
+            operations = client.operations.list(graph_id, _offset=offset)
+            ops += operations.items
+            if len(ops) < operations.metadata.pagination.total:
+                offset += operations.metadata.pagination.size
+            else:
+                break
+        return ops
 
     def update_operation(self, operation_id, state):
         client = get_rest_client()
