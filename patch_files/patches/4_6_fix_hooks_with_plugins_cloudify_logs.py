diff --git a/cloudify/logs.py b/cloudify/logs.py
index f918bf2..7a1ddda 100644
--- a/cloudify/logs.py
+++ b/cloudify/logs.py
@@ -45,7 +45,7 @@ def message_context_from_cloudify_context(ctx):
         'task_target': ctx.task_target,
         'operation': ctx.operation.name,
         'plugin': ctx.plugin,
-        'tenant_name': ctx.tenant_name,
+        'tenant': ctx.tenant,
     }
     if ctx.type == constants.NODE_INSTANCE:
         context['node_id'] = ctx.instance.id
@@ -66,7 +66,7 @@ def message_context_from_workflow_context(ctx):
         'deployment_id': ctx.deployment.id,
         'execution_id': ctx.execution_id,
         'workflow_id': ctx.workflow_id,
-        'tenant_name': ctx.tenant_name,
+        'tenant': ctx.tenant,
     }
 
 
@@ -77,7 +77,7 @@ def message_context_from_sys_wide_wf_context(ctx):
         'deployment_id': None,
         'execution_id': ctx.execution_id,
         'workflow_id': ctx.workflow_id,
-        'tenant_name': ctx.tenant_name,
+        'tenant': ctx.tenant,
     }
 
 
