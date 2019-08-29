diff --git a/tests/integration_tests/tests/agentless_tests/test_snapshot.py b/tests/integration_tests/tests/agentless_tests/test_snapshot.py
index 9020efe8d..ef2b9e6e0 100644
--- a/tests/integration_tests/tests/agentless_tests/test_snapshot.py
+++ b/tests/integration_tests/tests/agentless_tests/test_snapshot.py
@@ -83,6 +83,53 @@ class TestSnapshot(AgentlessTestCase):
         execution = client.executions.get(execution.id)
         self.assertEqual(execution.status, ExecutionState.FAILED)
 
+    def test_4_4_snapshot_restore_with_bad_plugin_wgn_file(self):
+        snapshot_path = \
+            self._get_snapshot('snap_4_4_0_bad_plugin_wgn_file.zip')
+        self._upload_and_restore_snapshot(
+            snapshot_path,
+            desired_execution_status=Execution.TERMINATED,
+            error_execution_status=Execution.FAILED,
+            ignore_plugin_install_failure=True)
+
+        # Now make sure all the resources really exist in the DB
+        # Assert snapshot restored
+        self._assert_4_4_0_snapshot_restored_bad_plugin_no_deployments()
+
+    def test_4_4_snapshot_restore_with_bad_plugin_no_directory(self):
+        snapshot_path = \
+            self._get_snapshot('snap_4_4_0_bad_plugin_no_directory.zip')
+        self._upload_and_restore_snapshot(
+            snapshot_path,
+            desired_execution_status=Execution.TERMINATED,
+            error_execution_status=Execution.FAILED,
+            ignore_plugin_install_failure=True)
+
+        # Now make sure all the resources really exist in the DB
+        # Assert snapshot restored
+        self._assert_4_4_0_snapshot_restored_bad_plugin_no_deployments()
+
+    def test_4_4_snapshot_restore_with_bad_plugin_with_deps(self):
+        snapshot_path = self._get_snapshot(
+            'snap_4_4_0_bad_plugin_no_directory_with_deps.zip')
+        self._upload_and_restore_snapshot(
+            snapshot_path,
+            desired_execution_status=Execution.TERMINATED,
+            error_execution_status=Execution.FAILED,
+            ignore_plugin_install_failure=True)
+
+        # Now make sure all the resources really exist in the DB
+        # Assert snapshot restored
+        self._assert_4_4_0_snapshot_restored_bad_plugin_no_deployments()
+
+    def test_4_4_snapshot_restore_with_bad_plugin_fails(self):
+        snapshot_path = \
+            self._get_snapshot('snap_4_4_0_bad_plugin_no_directory.zip')
+        self._upload_and_restore_snapshot(
+            snapshot_path,
+            desired_execution_status=Execution.FAILED,
+            error_execution_status=Execution.CANCELLED)
+
     def test_4_2_snapshot_with_deployment(self):
         snapshot_path = self._get_snapshot('snap_4.2.0.zip')
         self._upload_and_restore_snapshot(snapshot_path)
@@ -175,6 +222,13 @@ class TestSnapshot(AgentlessTestCase):
         self._assert_3_3_1_snapshot_restored()
         self._assert_3_3_1_plugins_restored()
 
+    def _assert_4_4_0_snapshot_restored_bad_plugin_no_deployments(
+            self,
+            tenant_name=DEFAULT_TENANT_NAME):
+        self._assert_4_4_0_plugins_restored_bad_plugin_no_deployments(
+            tenant_name=tenant_name,
+        )
+
     def _assert_3_3_1_snapshot_restored(self,
                                         tenant_name=DEFAULT_TENANT_NAME):
         self._assert_snapshot_restored(
@@ -229,12 +283,12 @@ class TestSnapshot(AgentlessTestCase):
         self._upload_and_restore_snapshot(snapshot_path)
         blueprints = self.client.blueprints.list(
             _include=['id', 'visibility'])
-        assert blueprints[0]['id'] == 'blueprint_1' and \
-            blueprints[0]['visibility'] == 'tenant'
-        assert blueprints[1]['id'] == 'blueprint_2' and \
-            blueprints[1]['visibility'] == 'private'
-        assert blueprints[2]['id'] == 'blueprint_3' and \
-            blueprints[2]['visibility'] == 'private'
+        assert (blueprints[0]['id'] == 'blueprint_1' and
+                blueprints[0]['visibility'] == 'tenant')
+        assert (blueprints[1]['id'] == 'blueprint_2' and
+                blueprints[1]['visibility'] == 'private')
+        assert (blueprints[2]['id'] == 'blueprint_3' and
+                blueprints[2]['visibility'] == 'private')
 
     def test_v_4_2_restore_snapshot_with_resource_availability(self):
         """
@@ -246,12 +300,12 @@ class TestSnapshot(AgentlessTestCase):
         self._upload_and_restore_snapshot(snapshot_path)
         blueprints = self.client.blueprints.list(
             _include=['id', 'visibility'])
-        assert blueprints[0]['id'] == 'blueprint_1' and \
-            blueprints[0]['visibility'] == 'private'
-        assert blueprints[1]['id'] == 'blueprint_2' and \
-            blueprints[1]['visibility'] == 'tenant'
-        assert blueprints[2]['id'] == 'blueprint_3' and \
-            blueprints[2]['visibility'] == 'global'
+        assert (blueprints[0]['id'] == 'blueprint_1' and
+                blueprints[0]['visibility'] == 'private')
+        assert (blueprints[1]['id'] == 'blueprint_2' and
+                blueprints[1]['visibility'] == 'tenant')
+        assert (blueprints[2]['id'] == 'blueprint_3' and
+                blueprints[2]['visibility'] == 'global')
 
     def test_v_4_3_restore_snapshot_with_secrets(self):
         """
@@ -295,8 +349,8 @@ class TestSnapshot(AgentlessTestCase):
         assert secret_encrypted != 'top_secret'
 
         # The secrets values are not hidden
-        assert not secret_string.is_hidden_value and \
-            not secret_file.is_hidden_value
+        assert (not secret_string.is_hidden_value and
+                not secret_file.is_hidden_value)
 
     def _assert_snapshot_restored(self,
                                   blueprint_id,
@@ -348,6 +402,24 @@ class TestSnapshot(AgentlessTestCase):
         self.assertEqual(package_name_counts['cloudify-script-plugin'], 1)
         self.assertEqual(package_name_counts['cloudify-diamond-plugin'], 5)
 
+    def _assert_4_4_0_plugins_restored_bad_plugin_no_deployments(
+            self,
+            tenant_name=DEFAULT_TENANT_NAME):
+        """
+        Validate only 7 of the 8 plugins in the snapshot are being restored
+        also, no deployments have been restored
+        """
+        with self.client_using_tenant(self.client, tenant_name):
+            plugins = self.client.plugins.list()
+            deployments = self.client.deployments.list()
+        self.assertEqual(len(plugins), 7)
+        self.assertEqual(len(deployments), 0)
+        package_names = [plugin.package_name for plugin in plugins]
+        package_name_counts = Counter(package_names)
+        self.assertEqual(package_name_counts['cloudify-fabric-plugin'], 1)
+        self.assertEqual(package_name_counts['cloudify-script-plugin'], 1)
+        self.assertEqual(package_name_counts['cloudify-diamond-plugin'], 5)
+
     def _assert_deployment_restored(self,
                                     blueprint_id,
                                     deployment_id,
@@ -400,10 +472,14 @@ class TestSnapshot(AgentlessTestCase):
         tmp_file = os.path.join(self.workdir, name)
         return utils.download_file(snapshot_url, tmp_file)
 
-    def _upload_and_restore_snapshot(self,
-                                     snapshot_path,
-                                     tenant_name=DEFAULT_TENANT_NAME,
-                                     snapshot_id=None):
+    def _upload_and_restore_snapshot(
+            self,
+            snapshot_path,
+            tenant_name=DEFAULT_TENANT_NAME,
+            snapshot_id=None,
+            desired_execution_status=Execution.TERMINATED,
+            error_execution_status=Execution.FAILED,
+            ignore_plugin_install_failure=False):
         """Upload the snapshot and launch the restore workflow
         """
         snapshot_id = snapshot_id or self.SNAPSHOT_ID
@@ -412,12 +488,14 @@ class TestSnapshot(AgentlessTestCase):
                                            snapshot_id,
                                            rest_client)
         self.logger.debug('Restoring snapshot...')
-        execution = rest_client.snapshots.restore(snapshot_id)
+        execution = rest_client.snapshots.restore(
+            snapshot_id,
+            ignore_plugin_install_failure=ignore_plugin_install_failure)
         execution = self._wait_for_restore_execution_to_end(
             execution, rest_client)
-        if execution.status == Execution.FAILED:
+        if execution.status == error_execution_status:
             self.logger.error('Execution error: {0}'.format(execution.error))
-        self.assertEqual(Execution.TERMINATED, execution.status)
+        self.assertEqual(desired_execution_status, execution.status)
 
         # Wait for the restart of cloudify-restservice to end.
         # If the rest-security.conf file was changed the service is being
@@ -425,18 +503,6 @@ class TestSnapshot(AgentlessTestCase):
         # function _add_restart_command.
         time.sleep(5)
 
-    def _upload_and_validate_snapshot(self,
-                                      snapshot_path,
-                                      snapshot_id,
-                                      rest_client):
-        self.logger.debug('Uploading snapshot: {0}'.format(snapshot_path))
-        rest_client.snapshots.upload(snapshot_path, snapshot_id)
-        snapshot = rest_client.snapshots.get(snapshot_id)
-        self.logger.debug('Retrieved snapshot: {0}'.format(snapshot))
-        self.assertEquals(snapshot['id'], snapshot_id)
-        self.assertEquals(snapshot['status'], 'uploaded')
-        self.logger.info('Snapshot uploaded and validated')
-
     def _wait_for_restore_execution_to_end(
             self, execution, rest_client, timeout_seconds=60):
         """Can't use the `wait_for_execution_to_end` in the class because
