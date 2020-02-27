diff --git a/dsl_parser/tests/abstract_test_parser.py b/dsl_parser/tests/abstract_test_parser.py
index 0989c89..04b2515 100644
--- a/dsl_parser/tests/abstract_test_parser.py
+++ b/dsl_parser/tests/abstract_test_parser.py
@@ -188,21 +188,25 @@ imports:"""
                          resolver=resolver,
                          validate_version=validate_version)
 
-    def parse_1_0(self, dsl_string, resources_base_path=None):
+    def parse_1_0(self, dsl_string, resources_base_path=None, resolver=None):
         return self.parse(dsl_string, resources_base_path,
-                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_0)
+                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_0,
+                          resolver=resolver)
 
-    def parse_1_1(self, dsl_string, resources_base_path=None):
+    def parse_1_1(self, dsl_string, resources_base_path=None, resolver=None):
         return self.parse(dsl_string, resources_base_path,
-                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_1)
+                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_1,
+                          resolver=resolver)
 
-    def parse_1_2(self, dsl_string, resources_base_path=None):
+    def parse_1_2(self, dsl_string, resources_base_path=None, resolver=None):
         return self.parse(dsl_string, resources_base_path,
-                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_2)
+                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_2,
+                          resolver=resolver)
 
-    def parse_1_3(self, dsl_string, resources_base_path=None):
+    def parse_1_3(self, dsl_string, resources_base_path=None, resolver=None):
         return self.parse(dsl_string, resources_base_path,
-                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_3)
+                          dsl_version=self.BASIC_VERSION_SECTION_DSL_1_3,
+                          resolver=resolver)
 
     def parse_from_path(self, dsl_path, resources_base_path=None):
         return dsl_parse_from_path(dsl_path, resources_base_path)
