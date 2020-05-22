diff --git a/cloudify/_compat.py b/cloudify/_compat.py
index 4ea2d7f..47337ae 100644
--- a/cloudify/_compat.py
+++ b/cloudify/_compat.py
@@ -25,8 +25,10 @@ if PY2:
         from cStringIO import StringIO
     except ImportError:
         from StringIO import StringIO
+    text_type = unicode
 else:
     import queue
     from io import StringIO
+    text_type = str
 
-__all__ = ['PY2', 'queue', 'StringIO']
+__all__ = ['PY2', 'queue', 'StringIO', 'text_type']
