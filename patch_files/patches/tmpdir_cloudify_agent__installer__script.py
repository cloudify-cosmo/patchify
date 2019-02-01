diff --git a/cloudify_agent/installer/script.py b/cloudify_agent/installer/script.py
index b12e7db..83e517a 100644
--- a/cloudify_agent/installer/script.py
+++ b/cloudify_agent/installer/script.py
@@ -84,7 +84,8 @@ class AgentInstallationScriptBuilder(AgentInstaller):
             install=not self.cloudify_agent.is_provided,
             configure=True,
             start=True,
-            add_ssl_cert=add_ssl_cert
+            add_ssl_cert=add_ssl_cert,
+            tmpdir=self.cloudify_agent.tmpdir
         )
 
     def _get_local_cert_content(self):
@@ -173,7 +174,8 @@ class AgentInstallationScriptBuilder(AgentInstaller):
             link=script_url,
             sudo=sudo,
             ssl_cert_content=self._get_local_cert_content(),
-            ssl_cert_path=self._get_remote_ssl_cert_path()
+            ssl_cert_path=self._get_remote_ssl_cert_path(),
+            tmpdir=self.cloudify_agent.tmpdir
         )
         if not self.cloudify_agent.is_windows:
             args_dict['user'] = self.cloudify_agent['user']
