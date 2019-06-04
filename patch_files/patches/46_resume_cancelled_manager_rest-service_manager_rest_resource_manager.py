diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index b18d149..bd96447 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -469,7 +469,7 @@ class ResourceManager(object):
         else:
             return self.sm.delete(deployment)
 
-    def _reset_failed_operations(self, execution):
+    def _reset_operations(self, execution, from_states=None):
         """Force-resume the execution: restart failed operations.
 
         All operations that were failed are going to be retried,
@@ -479,9 +479,9 @@ class ResourceManager(object):
 
         :return: Whether to continue with running the execution
         """
-        execution.status = ExecutionState.STARTED
-        self.sm.update(execution, modified_attrs=('status',))
-
+        if from_states is None:
+            from_states = {cloudify_tasks.TASK_RESCHEDULED,
+                           cloudify_tasks.TASK_FAILED}
         tasks_graphs = self.sm.list(models.TasksGraph,
                                     filters={'execution': execution},
                                     get_all_results=True)
@@ -496,8 +496,7 @@ class ResourceManager(object):
             for operation in operations:
                 if operation.id in retried_operations:
                     continue
-                if operation.state in (cloudify_tasks.TASK_RESCHEDULED,
-                                       cloudify_tasks.TASK_FAILED):
+                if operation.state in from_states:
                     operation.state = cloudify_tasks.TASK_PENDING
                     operation.parameters['current_retries'] = 0
                     self.sm.update(operation,
@@ -505,19 +504,30 @@ class ResourceManager(object):
 
     def resume_execution(self, execution_id, force=False):
         execution = self.sm.get(models.Execution, execution_id)
-        if force:
-            if execution.status not in (ExecutionState.CANCELLED,
-                                        ExecutionState.FAILED):
-                raise manager_exceptions.ConflictError(
-                    'Cannot force-resume execution: `{0}` in state: `{1}`'
-                    .format(execution.id, execution.status))
-            self._reset_failed_operations(execution)
-
-        if execution.status != ExecutionState.STARTED:
+
+        if execution.status in {ExecutionState.CANCELLED,
+                                ExecutionState.FAILED}:
+            self._reset_operations(execution)
+            if force:
+                # with force, we resend all tasks which haven't finished yet
+                self._reset_operations(execution, from_states={
+                    cloudify_tasks.TASK_STARTED,
+                    cloudify_tasks.TASK_SENT,
+                    cloudify_tasks.TASK_SENDING,
+                })
+        elif force:
+            raise manager_exceptions.ConflictError(
+                'Cannot force-resume execution: `{0}` in state: `{1}`'
+                .format(execution.id, execution.status))
+        elif execution.status != ExecutionState.STARTED:
+            # not force and not cancelled/failed/started - invalid:
             raise manager_exceptions.ConflictError(
                 'Cannot resume execution: `{0}` in state: `{1}`'
                 .format(execution.id, execution.status))
-        self.sm.update(execution)
+
+        execution.status = ExecutionState.STARTED
+        execution.ended_at = None
+        self.sm.update(execution, modified_attrs=('status', 'ended_at'))
 
         workflow_id = execution.workflow_id
         deployment = execution.deployment
