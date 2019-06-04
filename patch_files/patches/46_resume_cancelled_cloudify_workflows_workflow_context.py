diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index af9adf9..33f53fd 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -1270,14 +1270,13 @@ class _TaskDispatcher(object):
         ping_handler = amqp_client.BlockingRequestResponseHandler(
             exchange=task['target'])
         client = self._get_client(task)
-        client.add_handler(handler)
         client.add_handler(ping_handler)
+        client.add_handler(handler)
         task.update({
             'client': client,
             'handler': handler,
             'ping_handler': ping_handler
         })
-        client.consume_in_thread()
         return task
 
     def _get_client(self, task):
@@ -1318,6 +1317,7 @@ class _TaskDispatcher(object):
 
         self._tasks.setdefault(client, {})[task['id']] = \
             (workflow_task, task, result)
+        client.consume_in_thread()
         return result
 
     def _set_task_state(self, workflow_task, state, event=None):
