diff --git a/dsl_parser/utils.py b/dsl_parser/utils.py
index 792905d..88b3930 100644
--- a/dsl_parser/utils.py
+++ b/dsl_parser/utils.py
@@ -333,7 +333,12 @@ def remove_namespace(value):
     return re.sub(value_namespace_format, '', value)
 
 
-def check_if_cloudify_type(type_name):
+def check_if_overridable_cloudify_type(type_name):
+    """
+    Checking if the type name has Cloudify prefix, which marks all
+    the Cloudify basic types that users can override.
+    For example: Install workflow should not be overridden.
+    """
     return type_name.startswith(constants.CLOUDIFY_TYPE_PREFIX)
 
 
