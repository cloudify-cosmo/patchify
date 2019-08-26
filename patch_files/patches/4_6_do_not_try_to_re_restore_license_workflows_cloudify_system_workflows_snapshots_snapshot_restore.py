diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 89d40f2..3f7367e 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -530,13 +530,18 @@ class SnapshotRestore(object):
                     ctx.tenant_name,
                 )
         finally:
-            postgres.restore_license_from_dump(self._tempdir)
+            if not self._license_exists(postgres):
+                postgres.restore_license_from_dump(self._tempdir)
 
         ctx.logger.info('Successfully restored database')
         # This is returned so that we can decide whether to restore the admin
         # user depending on whether we have the hash salt
         return admin_user_update_command
 
+    def _license_exists(self, postgres):
+        result = postgres.run_query('SELECT * FROM licenses;')
+        return False if '0' in result['status'] else True
+
     def _encrypt_secrets(self, postgres):
         # The secrets are encrypted
         if self._snapshot_version >= V_4_4_0:
