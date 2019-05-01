diff --git a/cloudify_agent/worker.py b/cloudify_agent/worker.py
index 96fca71..a2d1998 100644
--- a/cloudify_agent/worker.py
+++ b/cloudify_agent/worker.py
@@ -22,6 +22,7 @@ import logging
 import argparse
 import traceback
 import threading
+from distutils.version import StrictVersion
 
 from cloudify_agent.api import utils
 from cloudify_agent.api.factory import DaemonFactory
@@ -37,6 +38,7 @@ from cloudify_rest_client.exceptions import (
 
 from cloudify import dispatch, exceptions
 from cloudify.logs import setup_agent_logger
+from cloudify.utils import get_admin_api_token
 from cloudify.models_states import ExecutionState
 from cloudify.error_handling import serialize_known_exception
 from cloudify.state import current_workflow_ctx, workflow_ctx
@@ -81,8 +83,8 @@ class CloudifyOperationConsumer(TaskConsumer):
         super(CloudifyOperationConsumer, self).__init__(*args, **kwargs)
 
     def _print_task(self, ctx, action, status=None):
-        if ctx['type'] == 'workflow':
-            prefix = '{0} workflow'.format(action)
+        if ctx['type'] in ['workflow', 'hook']:
+            prefix = '{0} {1}'.format(action, ctx['type'])
             suffix = ''
         else:
             prefix = '{0} operation'.format(action)
@@ -319,12 +321,15 @@ class ServiceTaskConsumer(TaskConsumer):
                 'cloudify_agent' in node_instance.runtime_properties)
 
 
-class HookConsumer(TaskConsumer):
+class HookConsumer(CloudifyOperationConsumer):
     routing_key = 'events.hooks'
     HOOKS_CONFIG_PATH = '/opt/mgmtworker/config/hooks.conf'
 
-    def __init__(self, queue_name):
-        super(HookConsumer, self).__init__(queue_name, exchange_type='topic')
+    def __init__(self, queue_name, registry, max_workers=5):
+        super(HookConsumer, self).__init__(queue_name,
+                                           exchange_type='topic',
+                                           registry=registry,
+                                           threadpool_size=max_workers)
         self.queue = queue_name
         self.exchange = EVENTS_EXCHANGE_NAME
 
@@ -340,14 +345,8 @@ class HookConsumer(TaskConsumer):
         )
 
         try:
-            kwargs = hook.get('inputs') or {}
-            context = full_task['context']
-            context['event_type'] = event_type
-            context['timestamp'] = full_task['timestamp']
-            context['arguments'] = full_task['message']['arguments']
-            hook_function = get_func(hook['implementation'])
-            result = hook_function(context, **kwargs)
-            result = {'ok': True, 'result': result}
+            task = self._get_task(full_task, hook)
+            result = super(HookConsumer, self).handle_task(task)
         except Exception as e:
             result = {'ok': False, 'error': e.message}
             logger.error('{0!r}, while running the hook triggered by the '
@@ -378,6 +377,65 @@ class HookConsumer(TaskConsumer):
                     "compatible hook in the configuration".format(event_type))
         return None
 
+    def _get_task(self, full_task, hook):
+        hook_context, operation_context = self._get_contexts(
+            full_task,
+            hook['implementation']
+        )
+        task = {
+            'cloudify_task': {
+                'kwargs': {
+                    '__cloudify_context': operation_context
+                },
+                'args': [hook_context]
+            }
+        }
+        kwargs = hook.get('inputs') or {}
+        task['cloudify_task']['kwargs'].update(kwargs)
+        return task
+
+    def _get_contexts(self, full_task, implementation):
+        hook_context = full_task['context']
+        tenant = hook_context.pop('tenant')
+        tenant_name = tenant.get('name')
+        hook_context['tenant_name'] = tenant.get('name')
+        hook_context['event_type'] = full_task['event_type']
+        hook_context['timestamp'] = full_task['timestamp']
+        hook_context['arguments'] = full_task['message']['arguments']
+        operation_context = dict(
+            type='hook',
+            tenant=tenant,
+            no_ctx_kwarg=True,
+            task_target=self.queue,
+            tenant_name=tenant_name,
+            plugin=self._get_plugin(tenant_name, implementation)
+        )
+
+        if operation_context['plugin']:
+            split_task_name = implementation.split('.')[1:]
+            operation_context['task_name'] = '.'.join(split_task_name)
+        else:
+            operation_context['task_name'] = implementation
+        return hook_context, operation_context
+
+    def _get_plugin(self, tenant_name, implementation):
+        package_name = implementation.split('.')[0]
+        filter_plugin = {'package_name': package_name}
+        admin_api_token = get_admin_api_token()
+        rest_client = get_rest_client(tenant=tenant_name,
+                                      api_token=admin_api_token)
+        plugins = rest_client.plugins.list(**filter_plugin)
+        if not plugins:
+            return {}
+
+        plugins.sort(key=lambda p: StrictVersion(p.package_version),
+                     reverse=True)
+        return {
+            'package_name': package_name,
+            'package_version': plugins[0]['package_version'],
+            'visibility': plugins[0]['visibility']
+        }
+
 
 def _setup_excepthook(daemon_name):
     # Setting a new exception hook to catch any exceptions
@@ -494,7 +552,9 @@ def make_amqp_worker(args):
     ]
 
     if args.hooks_queue:
-        handlers.append(HookConsumer(args.hooks_queue))
+        handlers.append(HookConsumer(args.hooks_queue,
+                                     registry=operation_registry,
+                                     max_workers=args.max_workers))
 
     return AMQPConnection(handlers=handlers, name=args.name,
                           connect_timeout=None)
