diff --git a/cloudify_agent/api/pm/nssm.py b/cloudify_agent/api/pm/nssm.py
index 39cd548..dad2278 100644
--- a/cloudify_agent/api/pm/nssm.py
+++ b/cloudify_agent/api/pm/nssm.py
@@ -75,6 +75,8 @@ class NonSuckingServiceManagerDaemon(Daemon):
         self.startup_policy = params.get('startup_policy', 'auto')
         self.failure_reset_timeout = params.get('failure_reset_timeout', 60)
         self.failure_restart_delay = params.get('failure_restart_delay', 5000)
+        self.service_user = params.get('service_user', '')
+        self.service_password = params.get('service_password', '')
 
     def create_script(self):
         pass
@@ -92,6 +94,8 @@ class NonSuckingServiceManagerDaemon(Daemon):
             log_dir=self.log_dir,
             workdir=self.workdir,
             user=self.user,
+            service_user=self.service_user,
+            service_password=self.service_password,
             rest_host=self.rest_host,
             rest_port=self.rest_port,
             local_rest_cert_file=self.local_rest_cert_file,
