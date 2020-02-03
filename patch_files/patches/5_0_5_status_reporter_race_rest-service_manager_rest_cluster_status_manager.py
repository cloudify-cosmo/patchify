diff --git a/rest-service/manager_rest/cluster_status_manager.py b/rest-service/manager_rest/cluster_status_manager.py
index 1e61d93..677d717 100644
--- a/rest-service/manager_rest/cluster_status_manager.py
+++ b/rest-service/manager_rest/cluster_status_manager.py
@@ -15,6 +15,8 @@
 
 import copy
 import json
+import shutil
+import tempfile
 from os import path, makedirs
 from datetime import datetime, timedelta
 
@@ -540,8 +542,15 @@ def _create_statues_folder_if_needed():
 
 
 def _save_report(report_path, report_dict):
-    with open(report_path, 'w') as report_file:
+    # We write then move because the actual reports directory is replicated
+    # and thus changing the same file repeatedly can break replication
+    with tempfile.NamedTemporaryFile(
+        mode='w',
+        prefix='status-reporter-',
+        delete=False,
+    ) as report_file:
         json.dump(report_dict, report_file)
+    shutil.move(report_file.name, report_path)
 
 
 def _verify_syncthing_status():
