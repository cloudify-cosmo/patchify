diff --git a/cloudify/dispatch.py b/cloudify/dispatch.py
index 5ca3d60..4c96cd6 100644
--- a/cloudify/dispatch.py
+++ b/cloudify/dispatch.py
@@ -31,7 +31,10 @@ from contextlib import contextmanager
 
 from cloudify_rest_client.executions import Execution
 from cloudify_rest_client.constants import VisibilityState
-from cloudify_rest_client.exceptions import InvalidExecutionUpdateStatus
+from cloudify_rest_client.exceptions import (
+    InvalidExecutionUpdateStatus,
+    CloudifyClientError
+)
 
 from cloudify import logs
 from cloudify import exceptions
@@ -43,7 +46,7 @@ from cloudify import constants
 from cloudify.amqp_client_utils import AMQPWrappedThread
 from cloudify.manager import update_execution_status, get_rest_client
 from cloudify.workflows import workflow_context
-from cloudify.workflows import api
+from cloudify.workflows import api, tasks
 from cloudify.constants import LOGGING_CONFIG_FILE
 from cloudify.error_handling import (
     serialize_known_exception,
@@ -399,13 +402,35 @@ class OperationHandler(TaskHandler):
             # should be single `with` and comma-separate ctxmanagers,
             # but has to be nested for python 2.6 compat
             with self._amqp_client():
-                result = self._run_operation_func(ctx, kwargs)
+                with self._update_operation_state():
+                    result = self._run_operation_func(ctx, kwargs)
 
-        if ctx.operation._operation_retry:
-            raise ctx.operation._operation_retry
+            if ctx.operation._operation_retry:
+                raise ctx.operation._operation_retry
         return result
 
     @contextmanager
+    def _update_operation_state(self):
+        ctx = self.ctx
+        try:
+            ctx.update_operation(tasks.TASK_STARTED)
+        except CloudifyClientError as e:
+            if e.status_code != 404:
+                raise
+            # if we can't update the operation, the operation isn't stored
+            # and we shouldn't update it afterwards either
+            store = False
+        else:
+            store = True
+        try:
+            yield
+        finally:
+            if store:
+                state = tasks.TASK_RESCHEDULED \
+                    if ctx.operation._operation_retry else tasks.TASK_SUCCEEDED
+                ctx.update_operation(state)
+
+    @contextmanager
     def _amqp_client(self):
         # initialize an amqp client only when needed, ie. if the task is
         # not local
