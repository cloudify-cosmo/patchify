diff --git a/cloudify/plugins/workflows.py b/cloudify/plugins/workflows.py
index 5a29dba..2d1ff11 100644
--- a/cloudify/plugins/workflows.py
+++ b/cloudify/plugins/workflows.py
@@ -639,11 +639,11 @@ def _make_execute_operation_graph(ctx, operation, operation_kwargs,
 
 
 @workflow(resumable=True)
-def execute_operation(ctx, **kwargs):
+def execute_operation(ctx, *args, **kwargs):
     """ A generic workflow for executing arbitrary operations on nodes """
 
     graph = _make_execute_operation_graph(
-        ctx, name='execute_operation', **kwargs)
+        ctx, name='execute_operation', *args, **kwargs)
     graph.execute()
 
 
