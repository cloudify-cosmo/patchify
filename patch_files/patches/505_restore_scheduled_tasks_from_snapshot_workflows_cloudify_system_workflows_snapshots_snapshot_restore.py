diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 41641b3..c1f70a6 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -73,6 +73,7 @@ from .constants import (
     SECURITY_FILE_LOCATION,
     SECURITY_FILENAME
 )
+from .utils import is_later_than_now
 
 
 class SnapshotRestore(object):
@@ -145,6 +146,7 @@ class SnapshotRestore(object):
                 self._restore_agents()
                 self._restore_amqp_vhosts_and_users()
                 self._restore_deployment_envs(postgres)
+                self._restore_scheduled_executions()
 
                 if self._premium_enabled:
                     self._reconfigure_status_reporter(postgres)
@@ -928,6 +930,23 @@ class SnapshotRestore(object):
             str(user_id),
         ]).aggr_stdout.strip()
 
+    def _restore_scheduled_executions(self):
+        """Restore executions scheduled for a time after snapshot creation."""
+        for execution in self._client.executions.list(
+                _get_all_results=True, status=Execution.SCHEDULED):
+            if is_later_than_now(execution.scheduled_for):
+                ctx.logger.debug("Restoring execution %s (at %s)",
+                                 execution.workflow_id,
+                                 execution.scheduled_for)
+                self._client.executions.requeue(execution.id)
+            else:
+                self._client.executions.update(execution.id,
+                                               Execution.FAILED)
+                ctx.logger.warning("Execution %s scheduled for %s is "
+                                   "overdue. Marking as FAILED.",
+                                   execution.id,
+                                   execution.scheduled_for)
+
     @staticmethod
     def _mark_manager_restoring():
         with open(SNAPSHOT_RESTORE_FLAG_FILE, 'a'):
