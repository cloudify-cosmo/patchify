diff --git a/cloudify_premium/syncthing_utils.py b/cloudify_premium/syncthing_utils.py
index efdf9c6..159c53b 100644
--- a/cloudify_premium/syncthing_utils.py
+++ b/cloudify_premium/syncthing_utils.py
@@ -49,6 +49,19 @@ SYNCED_DIRECTORIES = CONFIG_DIRECTORIES + [
     ('mgmtworker-data', '/opt/mgmtworker/work', ['!admin_token']),
     ('cluster_statuses', '/opt/manager/cluster_statuses', None)
 ]
+DEFAULT_DIRECTORY_OPTIONS = {
+    'fsWatcherEnabled': True,
+    'rescanIntervalS': 600
+}
+
+DIRECTORY_OPTIONS = {
+    'cluster_statuses': {
+        'rescanIntervalS': RESCAN_INTERVAL_S,
+        'fsWatcherEnabled': False
+    }
+}
+
+
 RESOURCES_DIR = 'resources'
 PLUGINS_DIR = 'mgmtworker-plugins'
 
@@ -115,12 +128,15 @@ def mgmtworker_update_devices(rest_client=None, sync_folders=None):
             'name': str(manager['hostname'])
         })
 
-    folders = [{
-        'id': dir_id,
-        'path': path,
-        'rescanIntervalS': RESCAN_INTERVAL_S,
-        'devices': devices
-    } for dir_id, path, _ in sync_folders]
+    folders = []
+    for dir_id, path, _ in sync_folders:
+        folder = {
+            'id': dir_id,
+            'path': path,
+            'devices': devices
+        }
+        folder.update(DIRECTORY_OPTIONS.get(dir_id, DEFAULT_DIRECTORY_OPTIONS))
+        folders.append(folder)
 
     update_config({
         'devices': devices,
