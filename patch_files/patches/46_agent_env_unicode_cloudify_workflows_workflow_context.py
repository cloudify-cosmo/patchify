diff --git a/cloudify/workflows/workflow_context.py b/cloudify/workflows/workflow_context.py
index 33f53fd..cc73ea2 100644
--- a/cloudify/workflows/workflow_context.py
+++ b/cloudify/workflows/workflow_context.py
@@ -637,6 +637,23 @@ class _WorkflowContextBase(object):
         final_kwargs = self._merge_dicts(merged_from=kwargs,
                                          merged_into=operation_properties,
                                          allow_override=allow_kwargs_override)
+        if operation_executor != 'central_deployment_agent':
+            client = get_rest_client()
+            host = client.node_instances.get(node_context['host_id'])
+            try:
+                network = host.runtime_properties['cloudify_agent']\
+                    .get('network', 'default')
+                addr = self.bootstrap_context['cloudify_agent'][
+                    'networks'][network]
+            except KeyError:
+                pass
+            else:
+                env = node_context.setdefault('execution_env', {})
+                env.setdefault('REST_HOST', addr)
+                if task_name == 'script_runner.tasks.run':
+                    process = final_kwargs.setdefault('process', {})
+                    env = process.setdefault('env', {})
+                    env.setdefault('REST_HOST', addr)
 
         return self.execute_task(task_name,
                                  local=self.local,
