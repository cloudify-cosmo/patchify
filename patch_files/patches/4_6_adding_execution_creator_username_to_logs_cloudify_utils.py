diff --git a/cloudify/utils.py b/cloudify/utils.py
index 17632a9..e9c748a 100644
--- a/cloudify/utils.py
+++ b/cloudify/utils.py
@@ -230,6 +230,14 @@ def _get_current_context():
                        'context available.')
 
 
+def get_execution_creator_username():
+    """Returns the execution creator username to use in the logs"""
+    try:
+        return _get_current_context().execution_creator_username
+    except RuntimeError:
+        return None
+
+
 def get_rest_token():
     """
     Returns the auth token to use when calling the REST service
