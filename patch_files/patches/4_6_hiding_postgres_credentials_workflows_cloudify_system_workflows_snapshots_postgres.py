diff --git a/workflows/cloudify_system_workflows/snapshots/postgres.py b/workflows/cloudify_system_workflows/snapshots/postgres.py
index 7928c48..a647a3d 100644
--- a/workflows/cloudify_system_workflows/snapshots/postgres.py
+++ b/workflows/cloudify_system_workflows/snapshots/postgres.py
@@ -47,7 +47,7 @@ class Postgres(object):
     _COMPOSER_TABLES_TO_EXCLUDE = ['"SequelizeMeta"']
 
     def __init__(self, config):
-        ctx.logger.debug('Init Postgres config: {0}'.format(config))
+        self._print_postgres_config(config)
         self._bin_dir = config.postgresql_bin_path
         self._db_name = config.postgresql_db_name
         self._host = config.postgresql_host
@@ -74,7 +74,8 @@ class Postgres(object):
         # Don't change admin user during the restore or the workflow will
         # fail to correctly execute (the admin user update query reverts it
         # to the one from before the restore)
-        self._append_dump(dump_file, self._get_admin_user_update_query())
+        query, protected_query = self._get_admin_user_update_query()
+        self._append_dump(dump_file, query, protected_query)
 
         self._restore_dump(dump_file, self._db_name)
 
@@ -173,13 +174,16 @@ class Postgres(object):
         self._append_dump(dump_file, delete_current_execution_query)
 
     def _get_admin_user_update_query(self):
-        """Return a query that updates the admin user in the DB
+        """Returns a tuple of (query, print_query):
+        query - updates the admin user in the DB and
+        protected_query - hides the credentials for the logs file
         """
         username, password = self._get_admin_credentials()
-        return "UPDATE users " \
-               "SET username='{0}', password='{1}' " \
-               "WHERE id=0;" \
-               .format(username, password)
+        base_query = "UPDATE users " \
+                     "SET username='{0}', password='{1}' " \
+                     "WHERE id=0;"
+        return (base_query.format(username, password),
+                base_query.format('*'*8, '*'*8))
 
     def _get_execution_restore_query(self):
         """Return a query that creates an execution to the DB with the ID (and
@@ -296,8 +300,13 @@ class Postgres(object):
         run_shell(command)
 
     @staticmethod
-    def _append_dump(dump_file, query):
-        ctx.logger.debug('Adding to end of dump: {0}'.format(query))
+    def _append_dump(dump_file, query, protected_query=None):
+        """
+        `protected_query` is the same string as `query` only that it hides
+        sensitive information, e.g. username and password.
+        """
+        print_query = protected_query or query
+        ctx.logger.debug('Adding to end of dump: {0}'.format(print_query))
         with open(dump_file, 'a') as f:
             f.write('\n{0}\n'.format(query))
 
@@ -481,3 +490,12 @@ class Postgres(object):
     def restore_license_from_dump(self, tmp_dir):
         dump_file = os.path.join(tmp_dir, LICENSE_DUMP_FILE)
         self._restore_dump(dump_file, self._db_name, table='licenses')
+
+    @staticmethod
+    def _print_postgres_config(config):
+        postgres_password = config.postgresql_password
+        postgres_username = config.postgresql_username
+        config.postgresql_password = config.postgresql_username = '********'
+        ctx.logger.debug('Init Postgres config: {0}'.format(config))
+        config.postgresql_password = postgres_password
+        config.postgresql_username = postgres_username
