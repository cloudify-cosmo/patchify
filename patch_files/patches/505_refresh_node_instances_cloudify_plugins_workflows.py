diff --git a/cloudify/plugins/workflows.py b/cloudify/plugins/workflows.py
index 2e6344d..b1254ab 100644
--- a/cloudify/plugins/workflows.py
+++ b/cloudify/plugins/workflows.py
@@ -409,9 +409,6 @@ def scale_entity(ctx,
             # 'removed_ids_include_hint': []
         }
     })
-    # refresh node instances so that workflow_ctx.get_node_instance() can
-    # return the new node instance that were just created
-    ctx.refresh_node_instances()
     graph = ctx.graph_mode()
     try:
         ctx.logger.info('Deployment modification started. '
