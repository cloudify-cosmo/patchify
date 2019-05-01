diff --git a/cloudify/dispatch.py b/cloudify/dispatch.py
index 8c041de..5ca3d60 100644
--- a/cloudify/dispatch.py
+++ b/cloudify/dispatch.py
@@ -677,6 +677,7 @@ class WorkflowHandler(TaskHandler):
 
 TASK_HANDLERS = {
     'operation': OperationHandler,
+    'hook': OperationHandler,
     'workflow': WorkflowHandler
 }
 
