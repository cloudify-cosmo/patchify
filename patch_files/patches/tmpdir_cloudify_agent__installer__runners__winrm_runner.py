diff --git a/cloudify_agent/installer/runners/winrm_runner.py b/cloudify_agent/installer/runners/winrm_runner.py
index af67d78..d417fb0 100644
--- a/cloudify_agent/installer/runners/winrm_runner.py
+++ b/cloudify_agent/installer/runners/winrm_runner.py
@@ -61,7 +61,8 @@ class WinRMRunner(object):
                  uri=None,
                  transport=None,
                  validate_connection=True,
-                 logger=None):
+                 logger=None,
+                 tmpdir=None):
 
         logger = logger or setup_logger('WinRMRunner')
 
@@ -74,6 +75,7 @@ class WinRMRunner(object):
             'password': password,
             'transport': transport or DEFAULT_TRANSPORT
         }
+        self.tmpdir = tmpdir
 
         # Validations - [host, user, password]
         validate(self.session_config)
@@ -227,6 +229,8 @@ class WinRMRunner(object):
         :rtype: str
 
         """
+        if self.tmpdir is not None:
+            return self.tmpdir
         return self.run(
             '@powershell -Command "[System.IO.Path]::GetTempPath()"'
         ).std_out.strip()
