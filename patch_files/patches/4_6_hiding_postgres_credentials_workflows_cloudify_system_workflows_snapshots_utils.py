diff --git a/workflows/cloudify_system_workflows/snapshots/utils.py b/workflows/cloudify_system_workflows/snapshots/utils.py
index 58db6b8..c8eec5b 100644
--- a/workflows/cloudify_system_workflows/snapshots/utils.py
+++ b/workflows/cloudify_system_workflows/snapshots/utils.py
@@ -34,20 +34,18 @@ PYTHON_MANAGER_ENV = '/opt/manager/env/bin/python'
 SCHEMA_SCRIPT = '/opt/manager/resources/cloudify/migrations/schema.py'
 
 
-class DictToAttributes(object):
-    def __init__(self, dic):
-        self._dict = dic
+class DictToAttributes(dict):
+    def __init__(self, dictionary):
+        super(DictToAttributes, self).__init__(dictionary)
 
-    def __getattr__(self, name):
-        return self._dict[name]
+    def __getattr__(self, key):
+        return super(DictToAttributes, self).__getitem__(key)
+
+    def __setattr__(self, key, value):
+        super(DictToAttributes, self).__setitem__(key, value)
 
     def __str__(self):
-        try:
-            # try to convert to json,
-            # may fail on UTF-8 and stuff, don't sweat on it..
-            return json.dumps(self._dict)
-        except Exception:
-            return self._dict
+        return json.dumps(self)
 
 
 def copy_files_between_manager_and_snapshot(archive_root,
