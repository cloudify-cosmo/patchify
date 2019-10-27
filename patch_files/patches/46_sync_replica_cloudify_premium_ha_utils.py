diff --git a/cloudify_premium/ha/utils.py b/cloudify_premium/ha/utils.py
index 6c3ec6c..1b08040 100644
--- a/cloudify_premium/ha/utils.py
+++ b/cloudify_premium/ha/utils.py
@@ -472,6 +472,10 @@ class _ClusterOnlineChecker(_WithConsulClient):
         if psycopg2 is None:
             raise RuntimeError('psycopg2 is required to get candidates!')

+        _, all_db_nodes = self.consul_client.health.service('database')
+        all_nodes_count = len(all_db_nodes)
+        quorum = all_nodes_count // 2 + 1
+
         alive_services_nodes = self.get_passing_nodes('managerservices')
         reachable_consul_nodes = self.get_passing_nodes('consul')

@@ -484,6 +488,12 @@ class _ClusterOnlineChecker(_WithConsulClient):
             if candidate[1] == -1:
                 continue
             candidates.append(candidate)
+        if not candidates:
+            raise RuntimeError('No candidates')
+        if len(candidates) < quorum:
+            raise RuntimeError('Found only {0} candidates, but need at least '
+                               '{1} for majority'
+                               .format(len(candidates), quorum))
         return candidates


