diff --git a/cloudify/endpoint.py b/cloudify/endpoint.py
index ca97bba..b44c516 100644
--- a/cloudify/endpoint.py
+++ b/cloudify/endpoint.py
@@ -235,6 +235,10 @@ class ManagerEndpoint(Endpoint):
         else:
             return base_workdir
 
+    def update_operation(self, operation_id, state):
+        client = manager.get_rest_client()
+        client.operations.update(operation_id, state=state)
+
 
 class LocalEndpoint(Endpoint):
 
@@ -316,3 +320,7 @@ class LocalEndpoint(Endpoint):
 
     def get_workdir(self):
         return self.storage.get_workdir()
+
+    def update_operation(self, operation_id, state):
+        # operation storage is not supported for local
+        return None
