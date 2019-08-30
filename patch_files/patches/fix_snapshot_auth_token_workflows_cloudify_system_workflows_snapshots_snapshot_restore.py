diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 7007d4a..a705c33 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -28,7 +28,10 @@ import wagon
 from cloudify.workflows import ctx
 from cloudify.manager import get_rest_client
 from cloudify.exceptions import NonRecoverableError
-from cloudify.constants import FILE_SERVER_SNAPSHOTS_FOLDER
+from cloudify.constants import (
+    FILE_SERVER_SNAPSHOTS_FOLDER,
+    NEW_TOKEN_FILE_NAME,
+)
 from cloudify.utils import ManagerVersion, get_local_rest_certificate
 
 from cloudify_rest_client.executions import Execution
@@ -122,9 +125,11 @@ class SnapshotRestore(object):
             existing_plugins = self._get_existing_plugin_names()
 
             with Postgres(self._config) as postgres:
-                self._restore_db(postgres, schema_revision, stage_revision)
                 self._update_visibility(postgres)
                 self._restore_files_to_manager()
+                self._restore_db(postgres, schema_revision, stage_revision)
+                self._generate_new_rest_token()
+                self._restart_rest_service()
                 self._encrypt_secrets(postgres)
                 self._encrypt_rabbitmq_passwords(postgres)
                 self._restore_plugins(existing_plugins)
@@ -143,6 +148,62 @@ class SnapshotRestore(object):
             ctx.logger.debug('Removing temp dir: {0}'.format(self._tempdir))
             shutil.rmtree(self._tempdir)
 
+    def _generate_new_rest_token(self):
+        """
+        `snapshot restore` is triggered with a REST call that is authenticated
+        using security keys that are located in opt/manager/rest-security.conf.
+        During restore the rest-security.conf is changed, therefore any
+        restart of the REST service will result in authentication failure
+        (security config is loaded when the REST service starts).
+        Gunicorn restarts REST workers every 1000 calls.
+        Our solution:
+        1. At the earliest stage possible create a new valid REST token
+           using the new rest-security.conf file
+        2. Restart REST service
+        3. Continue with restore snapshot
+        (CY-767)
+        """
+        self._generate_new_token()
+        new_token = self._get_token_from_file()
+        # Replace old token with new one in the workflow context, and create
+        # new REST client
+        ctx._context['rest_token'] = new_token
+        self._client = get_rest_client()
+
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
+    def _generate_new_token(self):
+        dir_path = os.path.dirname(os.path.realpath(__file__))
+        script_path = os.path.join(dir_path, 'generate_new_rest_token.py')
+        command = [MANAGER_PYTHON, script_path, self._tempdir]
+        utils.run(command)
+
+    def _get_token_from_file(self):
+        """
+        The new token in saved at the snapshot`s temp dir (which is passed as
+        an argument to the 'generate_new_rest_token.py' script).
+        """
+        new_token_path = os.path.join(self._tempdir, NEW_TOKEN_FILE_NAME)
+        with open(new_token_path, 'r') as f:
+            new_token = f.read()
+        return new_token
+
     def _restore_deployment_envs(self, postgres):
         deps = utils.get_dep_contexts(self._snapshot_version)
         token_info = postgres.get_deployment_creator_ids_and_tokens()
