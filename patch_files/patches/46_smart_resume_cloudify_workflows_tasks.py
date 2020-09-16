diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index 80b14f1..f1d3e83 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -754,8 +754,10 @@ class LocalWorkflowTask(WorkflowTask):
 class NOPLocalWorkflowTask(LocalWorkflowTask):
 
     def __init__(self, workflow_context, **kwargs):
-        super(NOPLocalWorkflowTask, self).__init__(lambda: None,
-                                                   workflow_context)
+        kwargs.update(
+            workflow_context=workflow_context,
+            local_task=lambda: None)
+        super(NOPLocalWorkflowTask, self).__init__(**kwargs)
 
     @property
     def name(self):
@@ -763,12 +765,12 @@ class NOPLocalWorkflowTask(LocalWorkflowTask):
         return 'NOP'
 
     def _update_stored_state(self, state):
-        # the task is always stored as succeeded - nothing to update
+        # the task is always stored as pending - nothing to update
         pass
 
     def dump(self):
         stored = super(NOPLocalWorkflowTask, self).dump()
-        stored['state'] = TASK_SUCCEEDED
+        stored['state'] = TASK_PENDING
         stored['parameters'].update({
             'info': None,
             'error': None
