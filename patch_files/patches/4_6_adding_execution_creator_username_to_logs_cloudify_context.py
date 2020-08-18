diff --git a/cloudify/context.py b/cloudify/context.py
index 924ae8e..0dd0bff 100644
--- a/cloudify/context.py
+++ b/cloudify/context.py
@@ -786,6 +786,10 @@ class CloudifyContext(CommonContext):
         """This run of the operation is a resume of an interrupted run"""
         return self._context.get('resume', False)
 
+    @property
+    def execution_creator_username(self):
+        return self._context.get('execution_creator_username')
+
     def send_event(self, event):
         """
         Send an event to rabbitmq
