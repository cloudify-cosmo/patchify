diff --git a/dsl_parser/elements/imports.py b/dsl_parser/elements/imports.py
index 3a21c42..3cd1f2c 100644
--- a/dsl_parser/elements/imports.py
+++ b/dsl_parser/elements/imports.py
@@ -443,6 +443,12 @@ def _mark_key_value_holder_items(value_holder, field_name, field_value):
         setattr(v, field_name, field_value)
 
 
+def _merge_lists_with_no_duplicates(from_dict_holder, to_dict_holder):
+    for value_holder in from_dict_holder.value:
+        if value_holder not in to_dict_holder.value:
+            to_dict_holder.value.append(value_holder)
+
+
 def _merge_parsed_into_combined(combined_parsed_dsl_holder,
                                 parsed_imported_dsl_holder,
                                 version,
@@ -496,7 +502,7 @@ def _merge_parsed_into_combined(combined_parsed_dsl_holder,
                 3, msg.format(key_holder.value))
 
 
-def _merge_namespaced_elements(key_holder, namespace, value_holder):
+def _prepare_namespaced_elements(key_holder, namespace, value_holder):
     if isinstance(value_holder.value, dict):
         for v in value_holder.value.values():
             v.namespace = namespace
@@ -505,34 +511,98 @@ def _merge_namespaced_elements(key_holder, namespace, value_holder):
         # the sub elements with the namespace, but leaving the option
         # for the DSL element to not receive the namespace.
         value_holder.only_children_namespace = True
+
         value_holder.namespace = namespace
-    if not utils.check_if_cloudify_type(key_holder.value):
+    if not utils.check_if_overridable_cloudify_type(key_holder.value):
         key_holder.value = utils.generate_namespaced_value(
             namespace, key_holder.value)
 
 
+def _extend_list_with_namespaced_values(namespace,
+                                        from_list_holder,
+                                        to_list_holder):
+    if namespace:
+        for v in from_list_holder.value:
+            v.namespace = from_list_holder.namespace
+    to_list_holder.value.extend(from_list_holder.value)
+
+
+def _merge_node_templates_relationships(
+        key_holder, key_name, to_dict_holder, from_dict_holder):
+    def only_relationships_inside(element_holder):
+        return (constants.RELATIONSHIPS in element_holder and
+                len(element_holder.value) == 1)
+
+    if constants.RELATIONSHIPS in to_dict_holder:
+        only_relationships_in_source = only_relationships_inside(
+            from_dict_holder)
+        required_node_template_field = 'type'
+
+        if (len(to_dict_holder.value) == 1 and
+                (required_node_template_field in from_dict_holder or
+                 only_relationships_in_source)):
+            # If the current parsed yaml contains only relationships element,
+            # the user can only extend with more relationships or merge it
+            # with required field to a set a node template.
+                _extend_node_template(from_dict_holder, to_dict_holder)
+                return
+        elif only_relationships_in_source:
+            _extend_list_with_namespaced_values(
+                from_dict_holder[constants.RELATIONSHIPS].namespace,
+                from_dict_holder[constants.RELATIONSHIPS],
+                to_dict_holder[constants.RELATIONSHIPS])
+            return
+    raise exceptions.DSLParsingLogicException(
+        4, "Import failed: Could not merge '{0}' due to conflict "
+           "on '{1}'".format(key_name, key_holder.value))
+
+
+def _extend_node_template(from_dict_holder, to_dict_holder):
+    for key_holder, value_holder in from_dict_holder.value.items():
+        if (isinstance(value_holder.value, dict) or
+                isinstance(value_holder.value, str)):
+            to_dict_holder.value[key_holder] = value_holder
+        elif (isinstance(value_holder.value, list) and
+              key_holder.value == constants.RELATIONSHIPS):
+            _extend_list_with_namespaced_values(
+                value_holder.namespace,
+                value_holder,
+                to_dict_holder.value[key_holder])
+
+
 def _merge_into_dict_or_throw_on_duplicate(from_dict_holder,
                                            to_dict_holder,
                                            key_name,
                                            namespace):
+    def cloudify_type(element_key_holder, element_value_holder):
+        """
+        If the element (key+value) is marked with Cloudify basic type flag
+        or the user overridden one.
+        """
+        return (element_value_holder.is_cloudify_type or
+                utils.check_if_overridable_cloudify_type(
+                    element_key_holder.value))
+
     for key_holder, value_holder in from_dict_holder.value.items():
+        if namespace and not value_holder.is_cloudify_type:
+            _prepare_namespaced_elements(key_holder, namespace, value_holder)
         _, to_value_holder = to_dict_holder.get_item(key_holder.value)
-        if not to_value_holder or to_value_holder.namespace != namespace:
-            if namespace and not value_holder.is_cloudify_type:
-                _merge_namespaced_elements(key_holder, namespace, value_holder)
+        if not to_value_holder or cloudify_type(key_holder, value_holder):
+            # If it's a new value or cloudify basic type which can be
+            # overwritten because it's the same.
             to_dict_holder.value[key_holder] = value_holder
-        elif not value_holder.is_cloudify_type:
+        elif key_name == constants.NODE_TEMPLATES:
+            _merge_node_templates_relationships(
+                key_holder,
+                key_name,
+                to_dict_holder.value[key_holder],
+                value_holder)
+        else:
             raise exceptions.DSLParsingLogicException(
                 4, "Import failed: Could not merge '{0}' due to conflict "
                    "on '{1}'".format(key_name, key_holder.value))
 
 
-def _merge_lists_with_no_duplicates(from_dict_holder, to_dict_holder):
-    for value_holder in from_dict_holder.value:
-        if value_holder not in to_dict_holder.value:
-            to_dict_holder.value.append(value_holder)
-
-
 class ImportsGraph(object):
 
     def __init__(self):
