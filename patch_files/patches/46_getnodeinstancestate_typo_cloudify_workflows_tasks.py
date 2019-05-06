diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index 59ffad8..b69bac8 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -1057,7 +1057,7 @@ class _GetNodeInstanceStateTask(_LocalTask):
         }
 
     def remote(self):
-        return get_node_instance(self._node_instance_idd).state
+        return get_node_instance(self._node_instance_id).state
 
     def local(self):
         instance = self.storage.get_node_instance(
