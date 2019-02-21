diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index d93249d..2ec19e2 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -453,7 +453,10 @@ class RemoteWorkflowTask(WorkflowTask):
             return cloudify_agent, self._get_tenant_dict(tenant, client)
 
         # this node instance isn't the real agent, check if it proxies to one
-        node = client.nodes.get(deployment_id, host_node_instance.node_id)
+        node = client.nodes.get(
+            deployment_id,
+            host_node_instance.node_id,
+            evaluate_functions=True)
         try:
             remote = node.properties['agent_config']['extra']['proxy']
             proxy_deployment = remote['deployment']
