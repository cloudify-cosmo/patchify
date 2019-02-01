diff --git a/cloudify_agent/installer/config/agent_config.py b/cloudify_agent/installer/config/agent_config.py
index 9f9e48b..48ad0f3 100644
--- a/cloudify_agent/installer/config/agent_config.py
+++ b/cloudify_agent/installer/config/agent_config.py
@@ -123,6 +123,13 @@ class CloudifyAgentConfig(dict):
     def is_windows(self):
         return self['windows']
 
+    @property
+    def tmpdir(self):
+        try:
+            return self['env'][cloudify_utils.CFY_EXEC_TEMPDIR_ENVVAR]
+        except KeyError:
+            return None
+
     def set_default_values(self):
         self._set_name()
         self.setdefault('network', constants.DEFAULT_NETWORK_NAME)
