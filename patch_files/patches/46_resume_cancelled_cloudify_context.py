diff --git a/cloudify/context.py b/cloudify/context.py
index 0ec9221..924ae8e 100644
--- a/cloudify/context.py
+++ b/cloudify/context.py
@@ -801,8 +801,14 @@ class CloudifyContext(CommonContext):
             self._provider_context = self._endpoint.get_provider_context()
         return self._provider_context
 
-    def get_resource(self,
-                     resource_path):
+    def update_operation(self, state):
+        """Update current operation state.
+
+        :param state: New operation state
+        """
+        self._endpoint.update_operation(self.task_id, state)
+
+    def get_resource(self, resource_path):
         """
         Retrieves a resource bundled with the blueprint as a string.
 
