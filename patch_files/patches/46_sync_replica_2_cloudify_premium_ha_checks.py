diff --git a/cloudify_premium/ha/checks.py b/cloudify_premium/ha/checks.py
index 9e2b994..39307ca 100644
--- a/cloudify_premium/ha/checks.py
+++ b/cloudify_premium/ha/checks.py
@@ -56,7 +56,8 @@ from cloudify_premium.ha import (cluster_status,
                                  sudo,
                                  systemd,
                                  users,
-                                 utils)
+                                 utils,
+                                 watch_handlers)
 
 logger = logging.getLogger(__name__)
 
@@ -142,32 +143,87 @@ def check_db_connection():
             cur.fetchall()
 
 
-@check(service_id='database', ttl=10, interval=3)
-def check_db_following():
+class _DBFollowingCheck(_Check):
     """Check if the local database is replicating from the current master."""
-    db = database.Database()
-    # check against the .next_master, so that we're already marked as failing
-    # during a switch
-    db_master = cluster_status.next_master
-    while True:
-        if node_status['name'] == db_master:
-            if not db.replication.is_already_master():
-                raise RuntimeError('Not master')
-            break
-        master_details = cluster_status.nodes[db_master]
-        master_ip = master_details['host_ip']
-        is_following = db.replication.is_already_following(master_ip)
-        # the `is_already_following` call might have taken a long time to
-        # run (up to connect_timeout - if the master is unreachable -
-        # 3 seconds); the master might have changed in the meantime - if
-        # so, try again with the current one
-        current_db_master = cluster_status.next_master
-        if current_db_master == db_master:
-            if is_following:
+    def __init__(self):
+        super(_DBFollowingCheck, self).__init__(
+            name='check_db_following',
+            func=self._check,
+            service_id='database',
+            ttl=10,
+            interval=3)
+        # amount of "not following" errors we've seen in a row. If we see
+        # too many of them, we'll attempt to fix it
+        self._not_following_errors = 0
+        # we'll attempt to fix after 60 "not following" errors,
+        # ie. about 3 minutes of failing
+        self._fix_threshold = 60
+
+    def _check(self):
+        db = database.Database()
+        # check against the .next_master, so that we're already marked as
+        # failing during a switch
+        db_master = cluster_status.next_master
+        while True:
+            if node_status['name'] == db_master:
+                if not db.replication.is_already_master():
+                    raise RuntimeError('Not master')
                 break
-            raise RuntimeError('Not following {0}'.format(master_ip))
-        # db_master changed during following check - loop again
-        db_master = current_db_master
+            master_details = cluster_status.nodes[db_master]
+            master_ip = master_details['host_ip']
+            is_following = db.replication.is_already_following(master_ip)
+            # the `is_already_following` call might have taken a long time to
+            # run (up to connect_timeout - if the master is unreachable -
+            # 3 seconds); the master might have changed in the meantime - if
+            # so, try again with the current one
+            current_db_master = cluster_status.next_master
+            if current_db_master == db_master:
+                if is_following:
+                    break
+                raise RuntimeError('Not following {0}'.format(master_ip))
+            # db_master changed during following check - loop again
+            db_master = current_db_master
+
+    def mark_passing(self):
+        self._not_following_errors = 0
+        return super(_DBFollowingCheck, self).mark_passing()
+
+    def mark_failing(self):
+        self._not_following_errors += 1
+        if self._not_following_errors > self._fix_threshold:
+            self._reset_following()
+        return super(_DBFollowingCheck, self).mark_failing()
+
+    def _reset_following(self):
+        """We've not been able to follow the current master for several
+        minutes, so force the follow handler to run again.
+
+        Grab the locks to make sure the follow isn't running right now,
+        and restart handler-runner when done.
+        """
+        master_watch = watch_handlers.NextMasterWatch()
+        next_master_watch = watch_handlers.MasterWatchCommand()
+        master_acquired = master_watch.lock.acquire(blocking=False)
+        if not master_acquired:
+            return
+        next_master_acquired = next_master_watch.lock.acquire(blocking=False)
+        if not next_master_acquired:
+            master_watch.lock.release()
+            return
+        try:
+            master_watch.stored_value = None
+            master_watch.stored_index = None
+            master_watch.save()
+            next_master_watch.stored_value = None
+            next_master_watch.stored_index = None
+            next_master_watch.save()
+            watch_handlers.HandlerRunner().restart()
+        finally:
+            master_watch.lock.release()
+            next_master_watch.lock.release()
+
+
+check_db_following = _DBFollowingCheck()
 
 
 @check(service_id='managerservices', ttl=20, interval=10)
