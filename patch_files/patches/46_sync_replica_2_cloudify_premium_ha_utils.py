diff --git a/cloudify_premium/ha/utils.py b/cloudify_premium/ha/utils.py
index 6c3ec6c..97d25ca 100644
--- a/cloudify_premium/ha/utils.py
+++ b/cloudify_premium/ha/utils.py
@@ -309,6 +309,11 @@ class ConsulLock(_WithConsulClient):
     # the same interface as the builtin python threading.Lock
     def __init__(self, name, timeout=5, interval=5, consul_client=None,
                  skip_exit=False):
+        # gotta import here unfortunately, see _WithConsulClient
+        from cloudify_premium.ha import consul
+        self._consul_client = consul.get_consul_client(
+            timeout=timeout * 4, retries=0)
+
         super(ConsulLock, self).__init__(consul_client=consul_client)
         self._name = name
         self._timeout = timeout
@@ -472,6 +477,10 @@ class _ClusterOnlineChecker(_WithConsulClient):
         if psycopg2 is None:
             raise RuntimeError('psycopg2 is required to get candidates!')
 
+        _, all_db_nodes = self.consul_client.health.service('database')
+        all_nodes_count = len(all_db_nodes)
+        quorum = all_nodes_count // 2 + 1
+
         alive_services_nodes = self.get_passing_nodes('managerservices')
         reachable_consul_nodes = self.get_passing_nodes('consul')
 
@@ -484,6 +493,12 @@ class _ClusterOnlineChecker(_WithConsulClient):
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
 
 
