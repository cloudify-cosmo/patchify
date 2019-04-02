diff --git a/cloudify_premium/ha/minority.py b/cloudify_premium/ha/minority.py
index 7cb9462..e69e6de 100644
--- a/cloudify_premium/ha/minority.py
+++ b/cloudify_premium/ha/minority.py
@@ -35,6 +35,7 @@ from cloudify_premium.ha import (cluster_status,
                                  consul,
                                  database,
                                  node_status,
+                                 options,
                                  sudo,
                                  systemd,
                                  users,
@@ -86,6 +87,9 @@ def watch_consul(check_interval_seconds, logger):
     consul_client = consul.get_consul_client()
 
     while True:
+        if not node_status.get(options.ALLOW_MINORITY):
+            time.sleep(check_interval_seconds)
+            continue
         if utils.minority_mode_enabled():
             reconnected = _check_reconnect(consul_client)
 
