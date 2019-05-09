diff --git a/workflows/cloudify_system_workflows/snapshots/utils.py b/workflows/cloudify_system_workflows/snapshots/utils.py
index a05dab7..58db6b8 100644
--- a/workflows/cloudify_system_workflows/snapshots/utils.py
+++ b/workflows/cloudify_system_workflows/snapshots/utils.py
@@ -352,8 +352,10 @@ def db_schema(revision, config=None):
 
     """
     db_schema_downgrade(revision, config=config)
-    yield
-    db_schema_upgrade(config=config)
+    try:
+        yield
+    finally:
+        db_schema_upgrade(config=config)
 
 
 def db_schema_downgrade(revision='-1', config=None):
