diff --git a/cloudify_premium/ha/options.py b/cloudify_premium/ha/options.py
index 5144593..857446e 100644
--- a/cloudify_premium/ha/options.py
+++ b/cloudify_premium/ha/options.py
@@ -15,11 +15,15 @@ CHECK_TTL_MULTIPLIER = 'check_ttl_multiplier'
 CHECK_FAIL_FAST = checks.FAIL_FAST_OPTION
 CONSUL_RAFT_MULTIPLIER = 'consul_raft_multiplier'
 CLUSTER_SSL_ENABLED = 'cluster_ssl_enabled'
-
+ALLOW_MINORITY = 'allow_minority_mode'
 NODE_OPTIONS = [CHECK_FAIL_FAST, CHECK_TTL_MULTIPLIER, CONSUL_RAFT_MULTIPLIER]
 CLUSTER_OPTIONS = [CLUSTER_SSL_ENABLED]
 
 
+def _update_allow_minority(allow_minority):
+    node_status[ALLOW_MINORITY] = allow_minority
+
+
 def _update_check_fail_fast(check_fail_fast):
     node_status[CHECK_FAIL_FAST] = check_fail_fast
 
@@ -54,6 +58,7 @@ OPTION_HANDLERS = {
     CHECK_TTL_MULTIPLIER: checks.deploy_checks,
     CONSUL_RAFT_MULTIPLIER: _update_consul_raft_multiplier,
     CLUSTER_SSL_ENABLED: _update_ssl_enabled,
+    ALLOW_MINORITY: _update_allow_minority
 }
 
 
