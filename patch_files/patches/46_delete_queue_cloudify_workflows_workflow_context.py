diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 33f53fd..f054ee3 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -22,7 +22,6 @@ import Queue
 import time
 import logging
 
-import pika
 from proxy_tools import proxy
 
 from cloudify import amqp_client, context
@@ -59,7 +58,7 @@ from cloudify.logs import (CloudifyWorkflowLoggingHandler,
                            send_workflow_event,
                            send_sys_wide_wf_event)
 
-from cloudify.utils import _send_ping_task
+from cloudify.utils import is_agent_alive
 
 
 try:
@@ -1265,17 +1264,12 @@ class _TaskDispatcher(object):
                 'cloudify_task': {'kwargs': kwargs},
             }
         }
-        handler = amqp_client.CallbackRequestResponseHandler(
-            exchange=task['target'], queue=task['id'])
-        ping_handler = amqp_client.BlockingRequestResponseHandler(
-            exchange=task['target'])
+        handler = amqp_client.CallbackRequestResponseHandler(task['target'])
         client = self._get_client(task)
-        client.add_handler(ping_handler)
         client.add_handler(handler)
         task.update({
             'client': client,
-            'handler': handler,
-            'ping_handler': ping_handler
+            'handler': handler
         })
         return task
 
@@ -1292,20 +1286,15 @@ class _TaskDispatcher(object):
         return client
 
     def send_task(self, workflow_task, task):
-        handler, ping_handler = task['handler'], task['ping_handler']
-        if task['queue'] != MGMTWORKER_QUEUE:
-            response = _send_ping_task(task['target'], ping_handler)
-            if 'time' not in response:
-                raise exceptions.RecoverableError(
-                    'Timed out waiting for agent: {0}'
-                    .format(task['target']))
-        try:
-            handler.publish(task['task'], routing_key='operation',
-                            correlation_id=task['id'])
-        except pika.exceptions.ChannelClosed:
+        agent = task['target']
+        handler = task['handler']
+        if task['queue'] != MGMTWORKER_QUEUE \
+                and not is_agent_alive(agent, task['client'], connect=False):
             raise exceptions.RecoverableError(
-                'Could not send to agent {0} - channel does not exist yet'
-                .format(task['target']))
+                'Timed out waiting for agent: {0}'.format(agent))
+
+        handler.publish(task['task'], routing_key='operation',
+                        correlation_id=task['id'])
         self._logger.debug('Task [{0}] sent'.format(task['id']))
 
     def wait_for_result(self, workflow_task, task):
