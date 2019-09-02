diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index ecbba7d..c6a98bf 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -107,6 +107,8 @@ class SnapshotRestore(object):
         ctx.logger.debug('Going to restore snapshot, '
                          'snapshot_path: {0}'.format(snapshot_path))
         try:
+            self._disable_gunicorn_worker_restart()
+
             metadata = self._extract_snapshot_archive(snapshot_path)
             self._snapshot_version = ManagerVersion(metadata[M_VERSION])
             schema_revision = metadata.get(
@@ -142,6 +144,23 @@ class SnapshotRestore(object):
         finally:
             ctx.logger.debug('Removing temp dir: {0}'.format(self._tempdir))
             shutil.rmtree(self._tempdir)
+            self._enable_gunicorn_worker_restart()
+
+    def _disable_gunicorn_worker_restart(self):
+        utils.run([
+            'sudo', 'sed', '-i',
+            's/GUNICORN_MAX_REQUESTS=1000/GUNICORN_MAX_REQUESTS=0/',
+            '/etc/sysconfig/cloudify-restservice',
+        ])
+        self._restart_rest_service()
+
+    def _enable_gunicorn_worker_restart(self):
+        utils.run([
+            'sudo', 'sed', '-i',
+            's/GUNICORN_MAX_REQUESTS=0/GUNICORN_MAX_REQUESTS=1000/',
+            '/etc/sysconfig/cloudify-restservice',
+        ])
+        self._restart_rest_service()
 
     def __should_ignore_plugin_failure(self,
                                        message):
@@ -319,6 +338,24 @@ class SnapshotRestore(object):
         )
         validator.validate()
 
+    def _restart_rest_service(self):
+        restart_command = 'sudo systemctl restart cloudify-restservice'
+        utils.run(restart_command)
+        self._wait_for_rest_to_restart()
+
+    def _wait_for_rest_to_restart(self, timeout=60):
+        deadline = time.time() + timeout
+        while True:
+            time.sleep(0.5)
+            if time.time() > deadline:
+                raise NonRecoverableError(
+                    'Failed to restart cloudify-restservice.')
+            try:
+                self._client.manager.get_status()
+                break
+            except Exception:
+                pass
+
     def _restore_files_to_manager(self):
         ctx.logger.info('Restoring files from the archive to the manager')
         utils.copy_files_between_manager_and_snapshot(
