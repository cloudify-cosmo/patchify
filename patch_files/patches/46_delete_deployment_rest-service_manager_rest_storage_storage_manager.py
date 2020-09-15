diff --git a/rest-service/manager_rest/storage/storage_manager.py b/rest-service/manager_rest/storage/storage_manager.py
index c535fd4..30e38b0 100644
--- a/rest-service/manager_rest/storage/storage_manager.py
+++ b/rest-service/manager_rest/storage/storage_manager.py
@@ -581,11 +581,12 @@ class SQLStorageManager(object):
         self._validate_unique_resource_id_per_tenant(instance)
         return instance
 
-    def delete(self, instance):
+    def delete(self, instance, load_relationships=True):
         """Delete the passed instance
         """
         current_app.logger.debug('Delete {0}'.format(instance))
-        self._load_relationships(instance)
+        if load_relationships:
+            self._load_relationships(instance)
         db.session.delete(instance)
         self._safe_commit()
         return instance
