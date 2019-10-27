diff --git a/cloudify_premium/ha/resources/sudo_trampoline.py b/cloudify_premium/ha/resources/sudo_trampoline.py
index 57f3d2a..d3e5770 100644
--- a/cloudify_premium/ha/resources/sudo_trampoline.py
+++ b/cloudify_premium/ha/resources/sudo_trampoline.py
@@ -74,6 +74,18 @@ def update_db_settings(config, data_dir, cloudify_db, cloudify_user,
     subprocess.check_call(['systemctl', 'reload', 'cloudify-postgresql'])
 
 
+def synchronous_commit(config, data_dir):
+    # also enable replicated synchronous commit in postgres
+    cluster_conf_path = os.path.join(data_dir, 'postgresql.cluster.conf')
+    with open(cluster_conf_path, 'r+') as f:
+        data = f.read()
+        data = data.replace("'local'", "'on'")
+        f.seek(0)
+        f.truncate()
+        f.write(data)
+    subprocess.check_call(['systemctl', 'reload', 'cloudify-postgresql'])
+
+
 def reload_consul(config):
     subprocess.check_call(['systemctl', 'reload', 'cloudify-consul'])
 
@@ -181,6 +193,7 @@ handlers = {
     'nginx': update_nginx,
     'postgresql': update_db_settings,
     'reload_consul': reload_consul,
+    'synchronous_commit': synchronous_commit,
     'minority_toggle': minority_toggle,
     'partitioned_cluster_changed': partitioned_cluster_changed,
     'promote_db': promote_db,
@@ -212,6 +225,9 @@ update_db_settings.add_argument('--replication-user', required=True)
 
 
 reload_consul_parser = subparsers.add_parser('reload_consul')
+synchronous_commit_parser = subparsers.add_parser('synchronous_commit')
+synchronous_commit_parser.add_argument(
+    '--data-dir', required=True, dest='data_dir')
 
 minority_toggle_parser = subparsers.add_parser('minority_toggle')
 minority_toggle_parser.add_argument('--disable', default=False,
