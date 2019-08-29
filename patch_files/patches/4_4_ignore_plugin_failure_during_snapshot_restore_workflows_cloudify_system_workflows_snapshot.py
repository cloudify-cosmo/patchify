diff --git a/workflows/cloudify_system_workflows/snapshot.py b/workflows/cloudify_system_workflows/snapshot.py
index 9288f2b49..2988c0347 100644
--- a/workflows/cloudify_system_workflows/snapshot.py
+++ b/workflows/cloudify_system_workflows/snapshot.py
@@ -49,6 +49,7 @@ def restore(snapshot_id,
             no_reboot,
             premium_enabled,
             user_is_bootstrap_admin,
+            ignore_plugin_installation_failure,
             **kwargs):
     ctx.logger.info('Restoring snapshot `{0}`'.format(snapshot_id))
     ctx.logger.debug('Restoring snapshot config: {0}'.format(config))
@@ -62,7 +63,8 @@ def restore(snapshot_id,
         premium_enabled,
         user_is_bootstrap_admin,
         restore_certificates,
-        no_reboot
+        no_reboot,
+        ignore_plugin_installation_failure
     )
     restore_snapshot.restore()
 
