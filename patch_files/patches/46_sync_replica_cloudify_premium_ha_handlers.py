diff --git a/cloudify_premium/ha/handlers.py b/cloudify_premium/ha/handlers.py
index 45c2593..d033361 100644
--- a/cloudify_premium/ha/handlers.py
+++ b/cloudify_premium/ha/handlers.py
@@ -34,7 +34,7 @@ from cloudify_premium.ha import (agents,
 from cloudify_premium.ha.decorators import is_database_local_wrapper


-def handler(name=None, retries=10, priority=0):
+def handler(name=None, retries=float('inf'), priority=0):
     """Mark a handler with this decorator to alter the default retrying policy.

     You can also force a handler to run before or after others by changing
@@ -160,6 +160,9 @@ def disable_consul_bootstrap(new_cluster, old_cluster, **kwargs):
         consul_service = consul.Consul()
         consul_service.disable_bootstrap()

+    db = database.Database()
+    sudo.run(['synchronous_commit', '--data-dir', db.config.data_dir])
+

 @handler()
 @is_database_local_wrapper
@@ -196,8 +199,6 @@ def choose_new_master(new_nodes, old_nodes, logger, **kwargs):

         candidates = utils.get_candidates()
         logger.debug('Candidates: {0}'.format(candidates))
-        if not candidates:
-            raise RuntimeError('No candidates')

         best_candidate = max(candidates, key=lambda x: x[1])[0]
         logger.info('Best master candidate: {0}'.format(best_candidate))
@@ -223,7 +224,7 @@ def update_syncthing_config(new_nodes, old_nodes, logger, **kwargs):
     logger.debug('syncthing config updated')


-@handler()
+@handler(retries=3, priority=-10)
 def update_agents(_new, _old, logger, **kwargs):
     """The cluster has changed: make sure all agents have the current list.

