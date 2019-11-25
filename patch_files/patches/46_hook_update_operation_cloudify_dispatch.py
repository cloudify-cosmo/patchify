diff --git a/cloudify/dispatch.py b/cloudify/dispatch.py
index 3997814..a742e7b 100644
--- a/cloudify/dispatch.py
+++ b/cloudify/dispatch.py
@@ -708,9 +708,15 @@ class WorkflowHandler(TaskHandler):
             raise caught_error
 
 
+class HookHandler(OperationHandler):
+    @contextmanager
+    def _update_operation_state(self):
+        yield 
+
+
 TASK_HANDLERS = {
     'operation': OperationHandler,
-    'hook': OperationHandler,
+    'hook': HookHandler,
     'workflow': WorkflowHandler
 }
 
