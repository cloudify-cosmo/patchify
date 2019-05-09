diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 4b89dd3..89d40f2 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -513,21 +513,25 @@ class SnapshotRestore(object):
         ctx.logger.info('Restoring database')
         postgres.dump_license_to_file(self._tempdir)
         admin_user_update_command = 'echo No admin user to update.'
-        if self._snapshot_version >= V_4_0_0:
-            with utils.db_schema(schema_revision, config=self._config):
-                admin_user_update_command = postgres.restore(self._tempdir)
-            self._restore_stage(postgres, self._tempdir, stage_revision)
-            self._restore_composer(postgres, self._tempdir)
-        else:
-            if self._should_clean_old_db_for_3_x_snapshot():
-                postgres.clean_db()
+        try:
+            if self._snapshot_version >= V_4_0_0:
+                with utils.db_schema(schema_revision, config=self._config):
+                    admin_user_update_command = postgres.restore(
+                        self._tempdir,
+                    )
+                self._restore_stage(postgres, self._tempdir, stage_revision)
+                self._restore_composer(postgres, self._tempdir)
+            else:
+                if self._should_clean_old_db_for_3_x_snapshot():
+                    postgres.clean_db()
 
-            ElasticSearch.restore_db_from_pre_4_version(
-                self._tempdir,
-                ctx.tenant_name,
-            )
+                ElasticSearch.restore_db_from_pre_4_version(
+                    self._tempdir,
+                    ctx.tenant_name,
+                )
+        finally:
+            postgres.restore_license_from_dump(self._tempdir)
 
-        postgres.restore_license_from_dump(self._tempdir)
         ctx.logger.info('Successfully restored database')
         # This is returned so that we can decide whether to restore the admin
         # user depending on whether we have the hash salt
