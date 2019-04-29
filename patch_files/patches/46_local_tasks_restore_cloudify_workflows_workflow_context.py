diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index a528045..ce63fbf 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -26,10 +26,7 @@ import pika
 from proxy_tools import proxy
 
 from cloudify import amqp_client, context
-from cloudify.manager import (get_node_instance,
-                              update_node_instance,
-                              update_execution_status,
-                              get_bootstrap_context,
+from cloudify.manager import (get_bootstrap_context,
                               get_rest_client,
                               download_resource)
 from cloudify.workflows.tasks import (TASK_FAILED,
@@ -42,7 +39,12 @@ from cloudify.workflows.tasks import (TASK_FAILED,
                                       DEFAULT_TOTAL_RETRIES,
                                       DEFAULT_RETRY_INTERVAL,
                                       DEFAULT_SEND_TASK_EVENTS,
-                                      DEFAULT_SUBGRAPH_TOTAL_RETRIES)
+                                      DEFAULT_SUBGRAPH_TOTAL_RETRIES,
+                                      _SetNodeInstanceStateTask,
+                                      _GetNodeInstanceStateTask,
+                                      _SendNodeEventTask,
+                                      _SendWorkflowEventTask,
+                                      _UpdateExecutionStatusTask)
 from cloudify.constants import MGMTWORKER_QUEUE
 from cloudify import utils, logs, exceptions
 from cloudify.state import current_workflow_ctx
@@ -55,8 +57,7 @@ from cloudify.logs import (CloudifyWorkflowLoggingHandler,
                            SystemWideWorkflowLoggingHandler,
                            init_cloudify_logger,
                            send_workflow_event,
-                           send_sys_wide_wf_event,
-                           send_workflow_node_event)
+                           send_sys_wide_wf_event)
 
 from cloudify.utils import _send_ping_task
 
@@ -1148,17 +1149,6 @@ class CloudifyWorkflowContextHandler(object):
     def get_send_task_event_func(self, task):
         raise NotImplementedError('Implemented by subclasses')
 
-    def get_update_execution_status_task(self, new_status):
-        raise NotImplementedError('Implemented by subclasses')
-
-    def get_send_node_event_task(self, workflow_node_instance,
-                                 event, additional_context=None):
-        raise NotImplementedError('Implemented by subclasses')
-
-    def get_send_workflow_event_task(self, event, event_type, args,
-                                     additional_context=None):
-        raise NotImplementedError('Implemented by subclasses')
-
     def get_task(self, workflow_task, queue=None, target=None, tenant=None):
         raise NotImplementedError('Implemented by subclasses')
 
@@ -1166,14 +1156,6 @@ class CloudifyWorkflowContextHandler(object):
     def operation_cloudify_context(self):
         raise NotImplementedError('Implemented by subclasses')
 
-    def get_set_state_task(self,
-                           workflow_node_instance,
-                           state):
-        raise NotImplementedError('Implemented by subclasses')
-
-    def get_get_state_task(self, workflow_node_instance):
-        raise NotImplementedError('Implemented by subclasses')
-
     def send_workflow_event(self, event_type, message=None, args=None,
                             additional_context=None):
         raise NotImplementedError('Implemented by subclasses')
@@ -1214,6 +1196,27 @@ class CloudifyWorkflowContextHandler(object):
     def remove_operation(self, operation_id):
         raise NotImplementedError('Implemented by subclasses')
 
+    # factory methods for local tasks
+    # TODO: if possible, consider inlining those to simplify
+    def get_set_state_task(self, workflow_node_instance, state):
+        return _SetNodeInstanceStateTask(workflow_node_instance.id, state)
+
+    def get_get_state_task(self, workflow_node_instance):
+        return _GetNodeInstanceStateTask(workflow_node_instance.id)
+
+    def get_send_node_event_task(self, workflow_node_instance,
+                                 event, additional_context=None):
+        return _SendNodeEventTask(
+            workflow_node_instance.id, event, additional_context)
+
+    def get_send_workflow_event_task(self, event, event_type, args,
+                                     additional_context=None):
+        return _SendWorkflowEventTask(event, event_type, args,
+                                      additional_context)
+
+    def get_update_execution_status_task(self, new_status):
+        return _UpdateExecutionStatusTask(new_status)
+
 
 class _AsyncResult(object):
     NOTSET = object()
@@ -1369,21 +1372,6 @@ class RemoteContextHandler(CloudifyWorkflowContextHandler):
     def get_send_task_event_func(self, task):
         return events.send_task_event_func_remote
 
-    def get_update_execution_status_task(self, new_status):
-        def update_execution_status_task():
-            update_execution_status(self.workflow_ctx.execution_id, new_status)
-        return update_execution_status_task
-
-    def get_send_workflow_event_task(self, event, event_type, args,
-                                     additional_context=None):
-        @task_config(send_task_events=False)
-        def send_event_task():
-            self.send_workflow_event(event_type=event_type,
-                                     message=event,
-                                     args=args,
-                                     additional_context=additional_context)
-        return send_event_task
-
     def get_task(self, workflow_task, queue=None, target=None, tenant=None):
         # augment cloudify context with target and queue
         tenant = tenant or workflow_task.cloudify_context.get('tenant')
@@ -1405,23 +1393,6 @@ class RemoteContextHandler(CloudifyWorkflowContextHandler):
                 'bypass_maintenance': utils.get_is_bypass_maintenance(),
                 'rest_token': utils.get_rest_token()}
 
-    def get_set_state_task(self,
-                           workflow_node_instance,
-                           state):
-        @task_config(send_task_events=False)
-        def set_state_task():
-            node_state = get_node_instance(workflow_node_instance.id)
-            node_state.state = state
-            update_node_instance(node_state)
-            return node_state
-        return set_state_task
-
-    def get_get_state_task(self, workflow_node_instance):
-        @task_config(send_task_events=False)
-        def get_state_task():
-            return get_node_instance(workflow_node_instance.id).state
-        return get_state_task
-
     def download_deployment_resource(self,
                                      blueprint_id,
                                      deployment_id,
@@ -1525,17 +1496,6 @@ class RemoteCloudifyWorkflowContextHandler(RemoteContextHandler):
                             additional_context=additional_context,
                             out_func=logs.amqp_event_out)
 
-    def get_send_node_event_task(self, workflow_node_instance,
-                                 event, additional_context=None):
-        @task_config(send_task_events=False)
-        def send_event_task():
-            send_workflow_node_event(ctx=workflow_node_instance,
-                                     event_type='workflow_node_event',
-                                     message=event,
-                                     additional_context=additional_context,
-                                     out_func=logs.amqp_event_out)
-        return send_event_task
-
     @property
     def scaling_groups(self):
         if not self._scaling_groups:
@@ -1586,34 +1546,6 @@ class LocalCloudifyWorkflowContextHandler(CloudifyWorkflowContextHandler):
     def get_send_task_event_func(self, task):
         return events.send_task_event_func_local
 
-    def get_update_execution_status_task(self, new_status):
-        raise NotImplementedError(
-            'Update execution status is not supported for '
-            'local workflow execution')
-
-    def get_send_node_event_task(self, workflow_node_instance,
-                                 event, additional_context=None):
-        @task_config(send_task_events=False)
-        def send_event_task():
-            send_workflow_node_event(ctx=workflow_node_instance,
-                                     event_type='workflow_node_event',
-                                     message=event,
-                                     additional_context=additional_context,
-                                     out_func=logs.stdout_event_out)
-        return send_event_task
-
-    def get_send_workflow_event_task(self, event, event_type, args,
-                                     additional_context=None):
-        @task_config(send_task_events=False)
-        def send_event_task():
-            send_workflow_event(ctx=self.workflow_ctx,
-                                event_type=event_type,
-                                message=event,
-                                args=args,
-                                additional_context=additional_context,
-                                out_func=logs.stdout_event_out)
-        return send_event_task
-
     def get_task(self, workflow_task, queue=None, target=None, tenant=None):
         raise NotImplementedError('Not implemented by local workflow tasks')
 
@@ -1622,25 +1554,6 @@ class LocalCloudifyWorkflowContextHandler(CloudifyWorkflowContextHandler):
         return {'local': True,
                 'storage': self.storage}
 
-    def get_set_state_task(self,
-                           workflow_node_instance,
-                           state):
-        @task_config(send_task_events=False)
-        def set_state_task():
-            self.storage.update_node_instance(
-                workflow_node_instance.id,
-                state=state,
-                version=None)
-        return set_state_task
-
-    def get_get_state_task(self, workflow_node_instance):
-        @task_config(send_task_events=False)
-        def get_state_task():
-            instance = self.storage.get_node_instance(
-                workflow_node_instance.id)
-            return instance.state
-        return get_state_task
-
     def send_workflow_event(self, event_type, message=None, args=None,
                             additional_context=None):
         send_workflow_event(self.workflow_ctx,
