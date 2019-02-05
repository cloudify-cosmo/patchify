diff --git a/cloudify_agent/tests/installer/test_installation.py b/cloudify_agent/tests/installer/test_installation.py
index 161a41d..5100f0b 100644
--- a/cloudify_agent/tests/installer/test_installation.py
+++ b/cloudify_agent/tests/installer/test_installation.py
@@ -21,6 +21,8 @@ from cloudify_agent.tests.resources import get_resource
 
 from cloudify.workflows import local
 
+from cloudify_agent.installer import AgentInstaller
+
 
 class InstallAgentTest(TestCase):
     """
@@ -59,3 +61,14 @@ class InstallAgentTest(TestCase):
     def test_install_agent_windows_3_2(self):
         self._test_install_agent(
             'test-install-agent-blueprint-windows-3-2.yaml')
+
+    def test_create_process_management_options(self):
+        installer = AgentInstaller({
+            'process_management': {
+                'name': 'nssm',
+                'param1': 'value1',
+                'param2': 'value2with$sign'
+            }
+        })
+        result = installer._create_process_management_options()
+        self.assertEquals(result, "--param1=value1 --param2='value2with$sign'")
