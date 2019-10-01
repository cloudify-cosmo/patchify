diff --git a/cloudify_premium/ha/database.py b/cloudify_premium/ha/database.py
index 2f4237b..5ed70ce 100644
--- a/cloudify_premium/ha/database.py
+++ b/cloudify_premium/ha/database.py
@@ -280,7 +280,7 @@ class _DBConfig(object):
                                          'postgresql.cluster.conf')
         with open(cluster_conf_path, 'w') as f:
             utils.render_resource(f, 'resources/postgresql.cluster.conf',
-                                  obj=self)
+                                  obj=self, synchronous_commit='local')
         db_user = pwd.getpwnam(self._db._owner)
         os.chown(cluster_conf_path, db_user.pw_uid, db_user.pw_gid)
         return True
