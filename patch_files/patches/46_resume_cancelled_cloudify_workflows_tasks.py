diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index cf3aedc..80b14f1 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -421,6 +421,9 @@ class RemoteWorkflowTask(WorkflowTask):
         # can safely be rerun
         if state == TASK_SENDING:
             return
+        if self.cloudify_context['executor'] != 'host_agent' \
+                and state in TERMINATED_STATES:
+            return
         return super(RemoteWorkflowTask, self)._update_stored_state(state)
 
     def apply_async(self):
@@ -435,6 +438,9 @@ class RemoteWorkflowTask(WorkflowTask):
         # 2) this is a resume (state=sent|started) and the task is a central
         #    deployment agent task
         should_send = self._state == TASK_PENDING or self._should_resume()
+
+        if self.cloudify_context['executor'] == 'host_agent':
+            should_send = self._state == TASK_PENDING
         if self._state == TASK_PENDING:
             self.set_state(TASK_SENDING)
         try:
@@ -451,10 +457,13 @@ class RemoteWorkflowTask(WorkflowTask):
                     TASK_SENDING, self)
                 self.set_state(TASK_SENT)
                 self.workflow_context.internal.handler.send_task(self, task)
+            else:
+                task['ping_handler'].delete_queue(task['ping_handler'].queue)
             self.async_result = RemoteWorkflowTaskResult(self, async_result)
         except (exceptions.NonRecoverableError,
                 exceptions.RecoverableError) as e:
-            self.set_state(TASK_FAILED)
+            if self.cloudify_context['executor'] == 'host_agent':
+                self.set_state(TASK_FAILED)
             self.async_result = RemoteWorkflowErrorTaskResult(self, e)
         return self.async_result
 
