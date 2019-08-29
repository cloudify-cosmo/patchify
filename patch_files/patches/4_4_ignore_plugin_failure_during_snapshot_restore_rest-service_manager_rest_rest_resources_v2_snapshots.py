diff --git a/rest-service/manager_rest/rest/resources_v2/snapshots.py b/rest-service/manager_rest/rest/resources_v2/snapshots.py
index ce3d529f9..a8a00ac99 100644
--- a/rest-service/manager_rest/rest/resources_v2/snapshots.py
+++ b/rest-service/manager_rest/rest/resources_v2/snapshots.py
@@ -254,7 +254,8 @@ class SnapshotsIdRestore(SecuredResource):
     def post(self, snapshot_id):
         _verify_no_multi_node_cluster(action="restore snapshot")
         request_dict = rest_utils.get_json_and_verify_params(
-            {'recreate_deployments_envs'}
+            {'recreate_deployments_envs',
+             'ignore_plugin_installation_failure'}
         )
         recreate_deployments_envs = rest_utils.verify_and_convert_bool(
             'recreate_deployments_envs',
@@ -273,6 +274,11 @@ class SnapshotsIdRestore(SecuredResource):
             'no_reboot',
             request_dict.get('no_reboot', 'false')
         )
+        ignore_plugin_installation_failure = \
+            rest_utils.verify_and_convert_bool(
+                'ignore_plugin_installation_failure',
+                request_dict.get('ignore_plugin_installation_failure', 'false')
+            )
         if no_reboot and not restore_certificates:
             raise manager_exceptions.BadParametersError(
                 '`no_reboot` is only relevant when `restore_certificates` is '
@@ -287,6 +293,7 @@ class SnapshotsIdRestore(SecuredResource):
             bypass_maintenance,
             timeout,
             restore_certificates,
-            no_reboot
+            no_reboot,
+            ignore_plugin_installation_failure
         )
         return execution, 200
