diff --git a/cloudify_agent/installer/config/agent_config.py b/cloudify_agent/installer/config/agent_config.py
index 881b58f..a0c5913 100644
--- a/cloudify_agent/installer/config/agent_config.py
+++ b/cloudify_agent/installer/config/agent_config.py
@@ -361,9 +361,6 @@ class CloudifyAgentConfig(dict):
                 cloudify_utils.get_broker_ssl_cert_path()
 
     def _set_package_url(self, runner):
-        if self.get('package_url'):
-            return
-
         agent_package_name = None
 
         if self.is_windows:
