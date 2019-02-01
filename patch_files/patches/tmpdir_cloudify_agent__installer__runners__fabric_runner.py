diff --git a/cloudify_agent/installer/runners/fabric_runner.py b/cloudify_agent/installer/runners/fabric_runner.py
index c3a399b..fef43cb 100644
--- a/cloudify_agent/installer/runners/fabric_runner.py
+++ b/cloudify_agent/installer/runners/fabric_runner.py
@@ -55,7 +55,8 @@ class FabricRunner(object):
                  port=None,
                  password=None,
                  validate_connection=True,
-                 fabric_env=None):
+                 fabric_env=None,
+                 tmpdir=None):
 
         # logger
         self.logger = logger or setup_logger('fabric_runner')
@@ -69,6 +70,7 @@ class FabricRunner(object):
         self.user = user
         self.host = host
         self.key = key
+        self.tmpdir = tmpdir
 
         # fabric environment
         self.env = self._set_env()
@@ -277,6 +279,8 @@ class FabricRunner(object):
             flags.append('-u')
         if directory:
             flags.append('-d')
+        if self.tmpdir is not None:
+            flags.append('-p "{0}"'.format(self.tmpdir))
         return self.run('mktemp {0}'
                         .format(' '.join(flags)),
                         **attributes).std_out.rstrip()
