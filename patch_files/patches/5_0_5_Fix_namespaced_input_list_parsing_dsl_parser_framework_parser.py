diff --git a/dsl_parser/framework/parser.py b/dsl_parser/framework/parser.py
index e707f86..720c92f 100644
--- a/dsl_parser/framework/parser.py
+++ b/dsl_parser/framework/parser.py
@@ -286,12 +286,16 @@ class Context(object):
                 holder_key, holder_value = holder_element.get_item(k)
                 if hasattr(holder_value, SKIP_NAMESPACE_FLAG):
                     return
-                if k == 'get_input':
+                if k == 'get_input' and not isinstance(v, list):
                     namespaced_value =\
                         utils.generate_namespaced_value(namespace, v)
                     element[k] = namespaced_value
                     holder_element.value[holder_key].value = namespaced_value
                     holder_value.skip_namespace = True
+                elif k == 'get_input' and isinstance(v, list):
+                    if isinstance(v[0], text_type):
+                        element[k][0] =\
+                            utils.generate_namespaced_value(namespace, v[0])
                 elif k == 'get_property' or k == 'get_attribute':
                     set_namespace_node_intrinsic_functions(
                         namespace,
