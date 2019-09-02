diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 40d412b17..ecbba7d9d 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -69,7 +69,6 @@ from .constants import (
 
 
 class SnapshotRestore(object):
-
     SCHEMA_REVISION_4_0 = '333998bc1627'
 
     def __init__(self,
@@ -81,7 +80,8 @@ class SnapshotRestore(object):
                  premium_enabled,
                  user_is_bootstrap_admin,
                  restore_certificates,
-                 no_reboot):
+                 no_reboot,
+                 ignore_plugin_installation_failure):
         self._npm = Npm()
         self._config = utils.DictToAttributes(config)
         self._snapshot_id = snapshot_id
@@ -91,6 +91,8 @@ class SnapshotRestore(object):
         self._no_reboot = no_reboot
         self._premium_enabled = premium_enabled
         self._user_is_bootstrap_admin = user_is_bootstrap_admin
+        self._ignore_plugin_installation_failure = \
+            ignore_plugin_installation_failure
         self._post_restore_commands = []
 
         self._tempdir = None
@@ -141,9 +143,15 @@ class SnapshotRestore(object):
             ctx.logger.debug('Removing temp dir: {0}'.format(self._tempdir))
             shutil.rmtree(self._tempdir)
 
+    def __should_ignore_plugin_failure(self,
+                                       message):
+        return 'cloudify_agent.operations.install_plugins' in \
+               message and self._ignore_plugin_installation_failure
+
     def _restore_deployment_envs(self, postgres):
         deps = utils.get_dep_contexts(self._snapshot_version)
         token_info = postgres.get_deployment_creator_ids_and_tokens()
+        failed_deployments = []
         for tenant, deployments in deps:
             ctx.logger.info(
                 'Restoring deployment environments for {tenant}'.format(
@@ -152,36 +160,42 @@ class SnapshotRestore(object):
             )
             tenant_client = get_rest_client(tenant=tenant)
             for deployment_id, dep_ctx in deployments.iteritems():
-                ctx.logger.info('Restoring deployment {dep_id}'.format(
-                    dep_id=deployment_id,
-                ))
-                api_token = self._get_api_token(
-                    token_info[tenant][deployment_id]
-                )
-                with dep_ctx:
-                    dep = tenant_client.deployments.get(deployment_id)
-                    blueprint = tenant_client.blueprints.get(
-                        dep_ctx.blueprint.id,
-                    )
-                    tasks_graph = self._get_tasks_graph(
-                        dep_ctx,
-                        blueprint,
-                        dep,
-                        api_token,
+                try:
+                    ctx.logger.info('Restoring deployment {dep_id}'.format(
+                        dep_id=deployment_id,
+                    ))
+                    api_token = self._get_api_token(
+                        token_info[tenant][deployment_id]
                     )
-                    tasks_graph.execute()
-                    ctx.logger.info(
-                        'Successfully created deployment environment '
-                        'for deployment {deployment}'.format(
-                            deployment=deployment_id,
+                    with dep_ctx:
+                        dep = tenant_client.deployments.get(deployment_id)
+                        blueprint = tenant_client.blueprints.get(
+                            dep_ctx.blueprint.id,
                         )
-                    )
-            ctx.logger.info(
-                'Finished restoring deployment environments for '
-                '{tenant}'.format(
-                    tenant=tenant,
-                )
-            )
+                        tasks_graph = self._get_tasks_graph(
+                            dep_ctx,
+                            blueprint,
+                            dep,
+                            api_token,
+                        )
+                        tasks_graph.execute()
+                        ctx.logger.info(
+                            'Successfully created deployment environment '
+                            'for deployment {deployment}'.format(
+                                deployment=deployment_id,
+                            )
+                        )
+                except RuntimeError as re:
+                    if self.__should_ignore_plugin_failure(re.message):
+                        ctx.logger.warning('Failed to create deployment: {0},'
+                                           'ignore_plugin_installation_failure'
+                                           'flag used, proceeding...'
+                                           .format(deployment_id))
+                        ctx.logger.debug('Deployment creation error: {0}'
+                                         .format(re))
+                        failed_deployments.append(deployment_id)
+                    else:
+                        raise re
 
     def _restore_amqp_vhosts_and_users(self):
         subprocess.check_call(
@@ -218,9 +232,9 @@ class SnapshotRestore(object):
 
         if not os.path.exists(
                 os.path.join(archive_cert_dir, INTERNAL_CA_CERT_FILENAME)):
-            for source, target in [
-                    (INTERNAL_CERT_FILENAME, INTERNAL_CA_CERT_FILENAME),
-                    (INTERNAL_KEY_FILENAME, INTERNAL_CA_KEY_FILENAME)]:
+            for source, target in \
+                    [(INTERNAL_CERT_FILENAME, INTERNAL_CA_CERT_FILENAME),
+                     (INTERNAL_KEY_FILENAME, INTERNAL_CA_KEY_FILENAME)]:
                 source = os.path.join(CERT_DIR, source)
                 target = os.path.join(CERT_DIR, target)
                 command += 'cp {source} {target};'.format(
@@ -319,7 +333,7 @@ class SnapshotRestore(object):
         # if this snapshot version is the same as the manager version
         # or from 4.3 onwards we support stage upgrade
         if self._snapshot_version == self._manager_version or \
-           self._snapshot_version >= V_4_3_0:
+                self._snapshot_version >= V_4_3_0:
             stage_restore_override = True
         else:
             stage_restore_override = False
@@ -504,6 +518,7 @@ class SnapshotRestore(object):
 
         :param existing_plugins: Names of already installed plugins
         """
+
         def should_install(plugin):
             # Can't just do 'not in' as plugin is a dict
             hashable_existing = (frozenset(p) for p in existing_plugins)
@@ -555,9 +570,12 @@ class SnapshotRestore(object):
             shutil.copyfile(plugin['path'], temp_plugin)
 
         client.plugins.delete(plugin['id'], force=True)
-        client.plugins.upload(temp_plugin,
-                              visibility=plugin['visibility'])
-        os.remove(temp_plugin)
+        try:
+            client.plugins.upload(temp_plugin,
+                                  visibility=plugin['visibility'])
+        finally:
+            # In any case, failure or success, delete tmp* folder
+            os.remove(temp_plugin)
 
     def _wait_for_plugin_executions(self, client):
         while True:
@@ -576,10 +594,32 @@ class SnapshotRestore(object):
                 msg = ', '.join('{0} (state: {1})'
                                 .format(execution.id, execution.status))
                 ctx.logger.info(
-                    'Waiting for plugin install executions to finish: {0}'
-                    .format(msg))
+                    'Waiting for plugin install executions to finish: '
+                    '{0}'.format(msg))
                 time.sleep(3)
 
+    @staticmethod
+    def __remove_failed_plugins_footprints(client, failed_plugins):
+        for failed_plugin in failed_plugins:
+            # Removing failed plugins from the database and file server
+            try:
+                ctx.logger.info('Removing failed plugin footprints')
+                client.plugins.delete(failed_plugin['id'], force=True)
+            except Exception as ex:
+                ctx.logger.warning('Failed to delete plugin footprints {0} '
+                                   'with error: {1}. Proceeding...'
+                                   .format(failed_plugin, ex.message))
+
+    @staticmethod
+    def __log_message_for_plugin_restore(failed_plugins):
+        if not failed_plugins:
+            ctx.logger.info('Successfully restored plugins')
+        else:
+            plugin_installation_log_message = \
+                'Plugins: {0} have not been installed ' \
+                'successfully'.format(failed_plugins)
+            ctx.logger.warning(plugin_installation_log_message)
+
     def _restore_plugins(self, existing_plugins):
         """Install any plugins that weren't installed prior to the restore
 
@@ -587,16 +627,34 @@ class SnapshotRestore(object):
         """
         ctx.logger.info('Restoring plugins')
         plugins_to_install = self._get_plugins_to_install(existing_plugins)
+        failed_plugins = []
         for tenant, plugins in plugins_to_install.items():
             client = get_rest_client(tenant=tenant)
             plugins_tmp = tempfile.mkdtemp()
             try:
                 for plugin in plugins:
-                    self._restore_plugin(client, tenant, plugin, plugins_tmp)
+                    try:
+                        self._restore_plugin(client,
+                                             tenant,
+                                             plugin,
+                                             plugins_tmp)
+                    except Exception as ex:
+                        if self._ignore_plugin_installation_failure:
+                            ctx.logger.warning(
+                                'Failed to restore plugin: {0}, '
+                                'ignore-plugin-installation-failure flag '
+                                'used. Proceeding...'.format(plugin))
+                            ctx.logger.debug('Restore plugin failure error: '
+                                             '{0}'.format(ex))
+                            failed_plugins.append(plugin)
+                        else:
+                            raise ex
                 self._wait_for_plugin_executions(client)
+                SnapshotRestore.__remove_failed_plugins_footprints(
+                    client, failed_plugins)
             finally:
                 os.rmdir(plugins_tmp)
-        ctx.logger.info('Successfully restored plugins')
+        SnapshotRestore.__log_message_for_plugin_restore(failed_plugins)
 
     @staticmethod
     def _plugin_installable_on_current_platform(plugin):
