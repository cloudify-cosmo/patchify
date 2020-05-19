diff --git a/cloudify_premium/ha/syncthing.py b/cloudify_premium/ha/syncthing.py
index d71d3fc..b87ad37 100644
--- a/cloudify_premium/ha/syncthing.py
+++ b/cloudify_premium/ha/syncthing.py
@@ -235,7 +235,8 @@ def update_devices(sync_folders=None):
     folders = [{
         'id': dir_id,
         'path': path,
-        'rescanIntervalS': 15,
+        'fsWatcherEnabled': True,
+        'rescanIntervalS': 600,
         'devices': devices
     } for dir_id, path, _ in sync_folders]
 
