diff --git a/cloudify_premium/ha/handlers.py b/cloudify_premium/ha/handlers.py
index 1d3983b..45c2593 100644
--- a/cloudify_premium/ha/handlers.py
+++ b/cloudify_premium/ha/handlers.py
@@ -19,6 +19,8 @@ Those functions are called by consul as watch handlers, using click commands.
 """
 
 import time
+import functools
+import threading
 
 from cloudify_premium.ha import (agents,
                                  cluster_status,
@@ -50,71 +52,95 @@ def handler(name=None, retries=10, priority=0):
     return _deco
 
 
+def lock_toggle(lock, promoting):
+    def _decorator(f):
+        @functools.wraps(f)
+        def _inner(new_master, *args, **kwargs):
+            me = node_status['name']
+            if promoting and me != new_master:
+                return
+            if not promoting and me == new_master:
+                return
+
+            with lock:
+                if promoting and me != cluster_status.next_master:
+                    return
+                if not promoting and me == cluster_status.next_master:
+                    return
+
+                return f(new_master, *args, **kwargs)
+
+        return _inner
+    return _decorator
+
+
+DB_CHANGE_LOCK = threading.Lock()
+NGINX_CHANGE_LOCK = threading.Lock()
+SERVICES_CHANGE_LOCK = threading.Lock()
+
+
 @handler()
 @is_database_local_wrapper
+@lock_toggle(DB_CHANGE_LOCK, promoting=False)
 def follow_master_db(new_master, old_master, logger):
     retries = 20
     retry_interval = 1
-
     db = database.Database()
-    if node_status['name'] != new_master:
-        for retry in range(retries):
-            try:
-                logger.info('switch_master_db: following')
-                db.replication.standby_follow(cluster_status.master)
-            except Exception as e:
-                logger.warning('Error when switching db: {0} (retry {1}/{2})'
-                               .format(e, retry, retries))
-                time.sleep(retry_interval)
-                continue
-            else:
-                break
+
+    for retry in range(retries):
+        try:
+            logger.info('switch_master_db: following')
+            db.replication.standby_follow(cluster_status.master)
+        except Exception as e:
+            logger.warning('Error when switching db: {0} (retry {1}/{2})'
+                           .format(e, retry, retries))
+            time.sleep(retry_interval)
+            continue
+        else:
+            break
 
 
 @handler()
+@lock_toggle(DB_CHANGE_LOCK, promoting=True)
 def promote_master_db(new_master, old_master, logger):
     db = database.Database()
-    if node_status['name'] == new_master:
-        if node_status.get('db') != 'master':
-            logger.info('promote_master_db: promoting')
-            db.replication.standby_promote()
 
-        cluster_status.master = node_status['name']
+    if node_status.get('db') != 'master':
+        logger.info('promote_master_db: promoting')
+        db.replication.standby_promote()
+
+    cluster_status.master = node_status['name']
 
 
 @handler()
+@lock_toggle(SERVICES_CHANGE_LOCK, promoting=True)
 def start_master_services(new_master, old_master, logger, **kwargs):
     """If this node is the new master, but was a replica before, start the
     services.
     """
-    if new_master != node_status['name']:
-        return
     logger.info('toggle_master_services: promoting')
     sudo.run(['promote'])
 
 
 @handler()
+@lock_toggle(NGINX_CHANGE_LOCK, promoting=True)
 def promote_nginx(new_master, old_master, logger, **kwargs):
-    if new_master != node_status['name']:
-        return
     sudo.run(['nginx', '--allow'])
 
 
 @handler()
+@lock_toggle(SERVICES_CHANGE_LOCK, promoting=False)
 def stop_master_services(new_master, old_master, logger, **kwargs):
     """If this node is not the new master, stop the services.
     """
-    if new_master == node_status['name']:
-        return
     logger.info('toggle_master_services: stopping')
     master_ip = cluster_status.nodes[new_master]['host_ip']
     sudo.run(['follow', '--master', master_ip])
 
 
 @handler(priority=10)
+@lock_toggle(NGINX_CHANGE_LOCK, promoting=False)
 def lock_nginx(new_master, old_master, logger, **kwargs):
-    if new_master == node_status['name']:
-        return
     logger.info('lock_nginx: locking')
     sudo.run(['nginx', '--location', 'rest-location-locked.cloudify'])
 
