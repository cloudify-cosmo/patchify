diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 3f7367e..48e7741 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -395,34 +395,6 @@ class SnapshotRestore(object):
 
         return admin_account
 
-    def _restore_admin_user(self):
-        admin_account = self._load_admin_dump()
-        with Postgres(self._config) as postgres:
-            psql_command = ' '.join(postgres.get_psql_command())
-        psql_command += ' -c '
-        update_prefix = '"UPDATE users SET '
-        # Hardcoded uid as we only allow running restore on a clean manager
-        # at the moment, so admin must be the first user (ID=0)
-        update_suffix = ' WHERE users.id=0"'
-        # Discard the id, we don't need it
-        admin_account.pop('id')
-        updates = []
-        for column, value in admin_account.items():
-            if value:
-                updates.append("{column}='{value}'".format(
-                    column=column,
-                    value=value,
-                ))
-        updates = ','.join(updates)
-        updates = updates.replace('$', '\\$')
-        command = psql_command + update_prefix + updates + update_suffix
-        # We have to do this after the restore process or it'll break the
-        # workflow execution updating and thus cause the workflow to fail
-        self._post_restore_commands.append(command)
-        # recreate the admin REST token file
-        self._post_restore_commands.append(
-            'sudo {0}'.format(ADMIN_TOKEN_SCRIPT))
-
     def _get_admin_user_token(self):
         return self._load_admin_dump()['api_token_key']
 
@@ -862,8 +834,6 @@ class SnapshotRestore(object):
             with open(SECURITY_FILE_LOCATION, 'w') as security_conf_handle:
                 json.dump(rest_security_conf, security_conf_handle)
 
-        self._restore_admin_user()
-
     def _get_script_path(self, script_name):
         return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             script_name)
