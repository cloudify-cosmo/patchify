diff --git a/cloudify/plugins/workflows.py b/cloudify/plugins/workflows.py
index 5d65baf..b5bc5be 100644
--- a/cloudify/plugins/workflows.py
+++ b/cloudify/plugins/workflows.py
@@ -284,6 +284,7 @@ def scale_entity(ctx,
                  ignore_failure=False,
                  include_instances=None,
                  exclude_instances=None,
+                 abort_started=False,
                  **kwargs):
     """Scales in/out the subgraph of node_or_group_name.
 
@@ -310,7 +311,10 @@ def scale_entity(ctx,
     :param ignore_failure: ignore operations failures in uninstall workflow
     :param include_instances: Instances to include when scaling down
     :param exclude_instances: Instances to exclude when scaling down
+    :param abort_started: Remove any started deployment modifications
+                          created prior to this scaling workflow
     """
+
     include_instances = include_instances or []
     exclude_instances = exclude_instances or []
     if isinstance(include_instances, basestring):
@@ -379,6 +383,10 @@ def scale_entity(ctx,
                          .format(delta,
                                  scalable_entity_name,
                                  curr_num_instances))
+
+    if abort_started:
+        _abort_started_deployment_modifications(ctx, ignore_failure)
+
     modification = ctx.deployment.start_modification({
         scale_id: {
             'instances': planned_num_instances,
@@ -466,6 +474,30 @@ def scale_entity(ctx,
             raise
 
 
+def _abort_started_deployment_modifications(ctx, ignore_failure):
+    """Aborts any started deployment modifications running in this context.
+
+    :param ctx: cloudify context
+    :param ignore_failure: ignore operations failures in uninstall workflow
+    """
+    started_modifications = ctx.deployment.list_started_modifications()
+    graph = ctx.graph_mode()
+    for modification in started_modifications:
+        ctx.logger.info('Rolling back deployment modification. '
+                        '[modification_id=%s]', modification.id)
+        added_and_related = set(modification.added.node_instances)
+        added = set(i for i in added_and_related
+                    if i.modification == 'added')
+        related = added_and_related - added
+        if added:
+            lifecycle.uninstall_node_instances(
+                graph=graph,
+                node_instances=added,
+                ignore_failure=ignore_failure,
+                related_nodes=related,
+            )
+        modification.rollback()
+
 # Kept for backward compatibility with older versions of types.yaml
 @workflow
 def scale(ctx, node_id, delta, scale_compute, **kwargs):
