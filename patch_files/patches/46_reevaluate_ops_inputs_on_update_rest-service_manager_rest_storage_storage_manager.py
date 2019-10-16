diff --git a/rest-service/manager_rest/storage/storage_manager.py b/rest-service/manager_rest/storage/storage_manager.py
index 3486a8e..4266f94 100644
--- a/rest-service/manager_rest/storage/storage_manager.py
+++ b/rest-service/manager_rest/storage/storage_manager.py
@@ -113,7 +113,9 @@ class SQLStorageManager(object):
     def _add_value_filter(self, query, filters):
         for column, value in filters.iteritems():
             column, value = self._update_case_insensitive(column, value)
-            if isinstance(value, (list, tuple)):
+            if callable(value):
+                query = query.filter(value(column))
+            elif isinstance(value, (list, tuple)):
                 query = query.filter(column.in_(value))
             else:
                 query = query.filter(column == value)
