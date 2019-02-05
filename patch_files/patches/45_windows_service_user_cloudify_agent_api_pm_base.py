diff --git a/cloudify_agent/api/pm/base.py b/cloudify_agent/api/pm/base.py
index 909e908..f927025 100644
--- a/cloudify_agent/api/pm/base.py
+++ b/cloudify_agent/api/pm/base.py
@@ -245,8 +245,7 @@ class Daemon(object):
         self.min_workers = params.get('min_workers') or defaults.MIN_WORKERS
         self.max_workers = params.get('max_workers') or defaults.MAX_WORKERS
         self.workdir = params.get('workdir') or os.getcwd()
-        self.executable_temp_path = params.get('executable_temp_path') or \
-            get_exec_tempdir()
+        self.executable_temp_path = params.get('executable_temp_path')
 
         self.extra_env_path = params.get('extra_env_path')
         self.log_level = params.get('log_level') or defaults.LOG_LEVEL
