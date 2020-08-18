diff --git a/cloudify_agent/worker.py b/cloudify_agent/worker.py
index a2d1998..dc70d03 100644
--- a/cloudify_agent/worker.py
+++ b/cloudify_agent/worker.py
@@ -36,7 +36,7 @@ from cloudify_rest_client.exceptions import (
 
 )
 
-from cloudify import dispatch, exceptions
+from cloudify import dispatch, exceptions, state
 from cloudify.logs import setup_agent_logger
 from cloudify.utils import get_admin_api_token
 from cloudify.models_states import ExecutionState
@@ -82,32 +82,31 @@ class CloudifyOperationConsumer(TaskConsumer):
         self._registry = kwargs.pop('registry')
         super(CloudifyOperationConsumer, self).__init__(*args, **kwargs)
 
-    def _print_task(self, ctx, action, status=None):
-        if ctx['type'] in ['workflow', 'hook']:
-            prefix = '{0} {1}'.format(action, ctx['type'])
-            suffix = ''
-        else:
-            prefix = '{0} operation'.format(action)
-            suffix = '\n\tNode ID: {0}'.format(ctx.get('node_id'))
-
-        if status:
-            suffix += '\n\tStatus: {0}'.format(status)
-
-        tenant_name = ctx.get('tenant', {}).get('name')
-        logger.info(
-            '\n\t{prefix} on queue `{queue}` on tenant `{tenant}`:\n'
-            '\tTask name: {name}\n'
-            '\tExecution ID: {execution_id}\n'
-            '\tWorkflow ID: {workflow_id}{suffix}\n'.format(
-                tenant=tenant_name,
-                prefix=prefix,
-                name=ctx['task_name'],
-                queue=ctx.get('task_target'),
-                execution_id=ctx.get('execution_id'),
-                workflow_id=ctx.get('workflow_id'),
-                suffix=suffix
-            )
-        )
+    def _print_task(self, ctx, action, handler, status=None):
+        with state.current_ctx.push(handler.ctx):
+            if ctx['type'] in ['workflow', 'hook']:
+                prefix = '{0} {1}'.format(action, ctx['type'])
+                suffix = ''
+            else:
+                prefix = '{0} operation'.format(action)
+                suffix = '\n\tNode ID: {0}'.format(ctx.get('node_id'))
+
+            if status:
+                suffix += '\n\tStatus: {0}'.format(status)
+
+            tenant_name = ctx.get('tenant', {}).get('name')
+            logger.info(
+                '\n\t%(prefix)s on queue `%(queue)s` on tenant `%(tenant)s`:\n'
+                '\tTask name: %(name)s\n'
+                '\tExecution ID: %(execution_id)s\n'
+                '\tWorkflow ID: %(workflow_id)s%(suffix)s\n',
+                {'tenant': tenant_name,
+                 'prefix': prefix,
+                 'name': ctx['task_name'],
+                 'queue': ctx.get('task_target'),
+                 'execution_id': ctx.get('execution_id'),
+                 'workflow_id': ctx.get('workflow_id'),
+                 'suffix': suffix})
 
     def handle_task(self, full_task):
         execution_creator_id = full_task.get('execution_creator')
@@ -122,10 +121,11 @@ class CloudifyOperationConsumer(TaskConsumer):
                 # Execution can't currently start running, it has been queued.
                 return
 
-        self._print_task(ctx, 'Started handling')
         handler = self.handler(cloudify_context=ctx, args=task.get('args', []),
                                kwargs=task['kwargs'],
                                process_registry=self._registry)
+
+        self._print_task(ctx, 'Started handling', handler)
         try:
             rv = handler.handle_or_dispatch_to_subprocess_if_remote()
             result = {'ok': True, 'result': rv}
@@ -139,7 +139,7 @@ class CloudifyOperationConsumer(TaskConsumer):
                     repr(e), error['traceback']
                 )
             )
-        self._print_task(ctx, 'Finished handling', status)
+        self._print_task(ctx, 'Finished handling', handler, status)
         return result
 
     @staticmethod
