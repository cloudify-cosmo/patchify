diff --git a/cloudify_agent/installer/__init__.py b/cloudify_agent/installer/__init__.py
index 7e5d776..21811e9 100644
--- a/cloudify_agent/installer/__init__.py
+++ b/cloudify_agent/installer/__init__.py
@@ -20,6 +20,13 @@ import ntpath
 import copy
 import base64
 
+try:
+    # Python 3.3+
+    from shlex import quote
+except ImportError:
+    # Python 2.7
+    from pipes import quote
+
 from cloudify_agent.installer.runners.local_runner import LocalCommandRunner
 from cloudify.utils import (get_tenant,
                             setup_logger,
@@ -185,7 +192,7 @@ class AgentInstaller(object):
         # environment variable
         process_management.pop('name')
         for key, value in process_management.iteritems():
-            options.append('--{0}={1}'.format(key, value))
+            options.append("--{0}={1}".format(key, quote(value)))
 
         return ' '.join(options)
 
