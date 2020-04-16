diff --git a/cloudify_agent/installer/config/agent_config.py b/cloudify_agent/installer/config/agent_config.py
index 48ad0f3..195ee22 100644
--- a/cloudify_agent/installer/config/agent_config.py
+++ b/cloudify_agent/installer/config/agent_config.py
@@ -362,9 +362,6 @@ class CloudifyAgentConfig(dict):
                 cloudify_utils.get_broker_ssl_cert_path()
 
     def _set_package_url(self, runner):
-        if self.get('package_url'):
-            return
-
         agent_package_name = None
 
         if self.is_windows:
