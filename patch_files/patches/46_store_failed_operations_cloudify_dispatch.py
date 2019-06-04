diff --git a/cloudify/dispatch.py b/cloudify/dispatch.py
index 4c96cd6..3997814 100644
--- a/cloudify/dispatch.py
+++ b/cloudify/dispatch.py
@@ -424,10 +424,18 @@ class OperationHandler(TaskHandler):
             store = True
         try:
             yield
+            error = False
+        except Exception:
+            error = True
+            raise
         finally:
             if store:
-                state = tasks.TASK_RESCHEDULED \
-                    if ctx.operation._operation_retry else tasks.TASK_SUCCEEDED
+                if ctx.operation._operation_retry:
+                    state = tasks.TASK_RESCHEDULED
+                elif error:
+                    state = tasks.TASK_FAILED
+                else:
+                    state = tasks.TASK_SUCCEEDED
                 ctx.update_operation(state)
 
     @contextmanager
