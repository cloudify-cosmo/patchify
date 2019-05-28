diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index 2fea55c..16f2a53 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -117,6 +117,9 @@ class WorkflowTask(object):
         self.execute_after = time.time()
         self.stored = False

+        # ID of the task that is being retried by this task
+        self.retried_task = None
+
     @classmethod
     def restore(cls, ctx, graph, task_descr):
         params = task_descr.parameters
@@ -147,6 +150,7 @@ class WorkflowTask(object):
             'name': self.name,
             'state': self._state,
             'type': self.task_type,
+            'retried_task': self.retried_task,
             'parameters': {
                 'current_retries': self.current_retries,
                 'send_task_events': self.send_task_events,
@@ -313,6 +317,7 @@ class WorkflowTask(object):
         dup = self._duplicate()
         dup.execute_after = execute_after
         dup.current_retries = self.current_retries + 1
+        dup.retried_task = self.id
         if dup.cloudify_context and 'operation' in dup.cloudify_context:
             op_ctx = dup.cloudify_context['operation']
             op_ctx['retry_number'] = dup.current_retries
