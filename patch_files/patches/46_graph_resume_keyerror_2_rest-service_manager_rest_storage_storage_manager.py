diff --git a/rest-service/manager_rest/storage/storage_manager.py b/rest-service/manager_rest/storage/storage_manager.py
index 4266f94..c535fd4 100644
--- a/rest-service/manager_rest/storage/storage_manager.py
+++ b/rest-service/manager_rest/storage/storage_manager.py
@@ -357,7 +357,11 @@ class SQLStorageManager(object):
             offset = 0
 
         total = query.order_by(None).count()  # Fastest way to count
-        results = query.limit(size).offset(offset).all()
+        if get_all_results:
+            results = query.all()
+        else:
+            results = query.limit(size).offset(offset).all()
+
         return results, total, size, offset
 
     @staticmethod
