diff --git a/dsl_parser/elements/workflows.py b/dsl_parser/elements/workflows.py
index d031300..cd2e57f 100644
--- a/dsl_parser/elements/workflows.py
+++ b/dsl_parser/elements/workflows.py
@@ -63,10 +63,10 @@ class Workflow(Element):
         if isinstance(self.initial_value, str):
             operation_content = {'mapping': self.initial_value,
                                  'parameters': {}}
-            is_cascading = True
+            is_cascading = False
         else:
             operation_content = self.build_dict_result()
-            is_cascading = self.initial_value.get('is_cascading', True)
+            is_cascading = self.initial_value.get('is_cascading', False)
         return operation.process_operation(
             plugins=plugins,
             operation_name=self.name,
