diff --git a/workflows/cloudify_system_workflows/snapshots/postgres.py b/workflows/cloudify_system_workflows/snapshots/postgres.py
index 96848bf..7928c48 100644
--- a/workflows/cloudify_system_workflows/snapshots/postgres.py
+++ b/workflows/cloudify_system_workflows/snapshots/postgres.py
@@ -287,6 +287,7 @@ class Postgres(object):
         ctx.logger.debug('Restoring db dump file: {0}'.format(dump_file))
         command = self.get_psql_command(db_name)
         command.extend([
+            '-v', 'ON_ERROR_STOP=1',
             '--single-transaction',
             '-f', dump_file
         ])
