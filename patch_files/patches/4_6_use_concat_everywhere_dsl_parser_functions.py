diff --git a/dsl_parser/functions.py b/dsl_parser/functions.py
index bfbfd614..baf7169d 100644
--- a/dsl_parser/functions.py
+++ b/dsl_parser/functions.py
@@ -682,12 +682,6 @@ class Concat(Function):
                 'Using {0} requires using dsl version 1_1 or '
                 'greater, but found: {1} in {2}.'
                 .format(self.name, plan.version, self.path))
-        if self.scope not in [scan.NODE_TEMPLATE_SCOPE,
-                              scan.NODE_TEMPLATE_RELATIONSHIP_SCOPE,
-                              scan.OUTPUTS_SCOPE]:
-            raise ValueError('{0} cannot be used in {1}.'
-                             .format(self.name,
-                                     self.path))
 
     def evaluate(self, plan):
         for joined_value in self.joined:
