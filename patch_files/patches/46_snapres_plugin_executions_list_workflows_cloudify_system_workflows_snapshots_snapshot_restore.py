diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 3f7367e..a561283 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -707,6 +707,8 @@ class SnapshotRestore(object):
     def _wait_for_plugin_executions(self, client):
         while True:
             executions = client.executions.list(
+                _include=['id', 'workflow_id', 'status'],
+                workflow_id='install_plugin',
                 include_system_workflows=True,
                 _all_tenants=True,
                 _get_all_results=True
