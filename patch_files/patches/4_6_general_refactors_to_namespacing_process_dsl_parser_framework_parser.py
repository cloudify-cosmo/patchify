diff --git a/dsl_parser/framework/parser.py b/dsl_parser/framework/parser.py
index c7a368c..e707f86 100644
--- a/dsl_parser/framework/parser.py
+++ b/dsl_parser/framework/parser.py
@@ -305,13 +305,18 @@ class Context(object):
                     traverse_list(holder_element.value[holder_key], v)
 
         def should_add_namespace_to_string_leaf(element):
-            return \
-                (isinstance(element._initial_value, basestring) and
-                 element._initial_value not in
-                 constants.USER_PRIMITIVE_TYPES and
-                 not utils.check_if_cloudify_type(element._initial_value) and
-                 not hasattr(element.initial_value_holder,
-                             SKIP_NAMESPACE_FLAG) and
+            if not isinstance(element._initial_value, str):
+                return False
+            is_premitive_type = (element._initial_value in
+                                 constants.USER_PRIMITIVE_TYPES)
+            overridable_cloudify_type = \
+                utils.check_if_overridable_cloudify_type(
+                    element._initial_value)
+            should_skip_adding_namespace =\
+                hasattr(element.initial_value_holder, SKIP_NAMESPACE_FLAG)
+            return (not is_premitive_type and
+                    not overridable_cloudify_type and
+                    not should_skip_adding_namespace and
                     element.add_namespace_to_schema_elements)
 
         def set_leaf_namespace(element):
@@ -336,7 +341,9 @@ class Context(object):
         def should_add_element_namespace(element_holder):
             # Preventing of adding namespace prefix to cloudify
             # basic types.
-            return (not utils.check_if_cloudify_type(element_holder.value) and
+            overridable_cloudify_type =\
+                utils.check_if_overridable_cloudify_type(element_holder.value)
+            return (not overridable_cloudify_type and
                     not hasattr(element_holder, SKIP_NAMESPACE_FLAG))
 
         def set_element_namespace(element_namespace, element_holder):
