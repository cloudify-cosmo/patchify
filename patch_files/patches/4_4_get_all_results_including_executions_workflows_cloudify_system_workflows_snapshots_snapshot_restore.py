diff --git a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
index 40d412b17..efe4bc463 100644
--- a/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
+++ b/workflows/cloudify_system_workflows/snapshots/snapshot_restore.py
@@ -563,7 +563,8 @@ class SnapshotRestore(object):
         while True:
             executions = client.executions.list(
                 include_system_workflows=True,
-                _all_tenants=True
+                _all_tenants=True,
+                _get_all_results=True
             )
             waiting = []
             for execution in executions:
