diff --git a/dsl_parser/functions.py b/dsl_parser/functions.py
index bfbfd614..68cf101a 100644
--- a/dsl_parser/functions.py
+++ b/dsl_parser/functions.py
@@ -879,7 +879,7 @@ def _handler(evaluator, **evaluator_kwargs):
             return msg.format(kwargs['path'])
         return ""
 
-    @limit_recursion(10, args_to_str_func=_args_to_str_func)
+    @limit_recursion(50, args_to_str_func=_args_to_str_func)
     def handler(v, scope, context, path):
         evaluated_value = v
         scanned = False
