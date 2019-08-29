diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index d61f70277..83ba204f8 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -165,7 +165,8 @@ class ResourceManager(object):
                          bypass_maintenance,
                          timeout,
                          restore_certificates,
-                         no_reboot):
+                         no_reboot,
+                         ignore_plugin_installation_failure):
         # Throws error if no snapshot found
         snapshot = self.sm.get(models.Snapshot, snapshot_id)
         if snapshot.status == SnapshotState.FAILED:
@@ -184,6 +185,8 @@ class ResourceManager(object):
                 'timeout': timeout,
                 'restore_certificates': restore_certificates,
                 'no_reboot': no_reboot,
+                'ignore_plugin_installation_failure':
+                    ignore_plugin_installation_failure,
                 'premium_enabled': premium_enabled,
                 'user_is_bootstrap_admin': current_user.is_bootstrap_admin
             },
