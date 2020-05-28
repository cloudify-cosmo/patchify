diff --git a/cloudify/proxy/server.py b/cloudify/proxy/server.py
index 7e45201..dab4d3f 100644
--- a/cloudify/proxy/server.py
+++ b/cloudify/proxy/server.py
@@ -236,8 +236,11 @@ def process_ctx_request(ctx, args):
 def _desugar_attr(obj, attr):
     if not isinstance(attr, basestring):
         return None
-    if hasattr(obj, attr):
-        return attr
+    try:
+        if hasattr(obj, attr):
+            return attr
+    except UnicodeError:
+        return None
     attr = attr.replace('-', '_')
     if hasattr(obj, attr):
         return attr
