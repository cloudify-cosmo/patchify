diff --git a/dsl_parser/holder.py b/dsl_parser/holder.py
index fa4ee6a..19a33ca 100644
--- a/dsl_parser/holder.py
+++ b/dsl_parser/holder.py
@@ -61,6 +61,13 @@ class Holder(object):
         key_holder, value_holder = self.get_item(key)
         return value_holder is not None
 
+    def __getitem__(self, key):
+        key_holder, value = self.get_item(key)
+        if not value:
+            raise KeyError("The expected key {0} does not exists"
+                           .format(key_holder.value))
+        return value
+
     def get_item(self, key):
         if not isinstance(self.value, dict):
             raise ValueError('Value is expected to be of type dict while it'
