diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 01e812f..851c9c2 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -440,11 +440,12 @@ class ResourceManager(object):
                               in ExecutionState.END_STATES])))
         if not ignore_live_nodes:
             deplyment_id_filter = self.create_filters_dict(
-                deployment_id=deployment_id)
+                deployment_id=deployment_id,
+                state=lambda col: ~col.in_(['uninitialized', 'deleted'])
+            )
             node_instances = self.sm.list(
                 models.NodeInstance,
                 filters=deplyment_id_filter,
-                get_all_results=True
             )
             # validate either all nodes for this deployment are still
             # uninitialized or have been deleted
@@ -467,7 +468,7 @@ class ResourceManager(object):
         # Delete deployment data  DB (should only happen AFTER the workflow
         # finished successfully, hence the delete_db_mode flag)
         else:
-            return self.sm.delete(deployment)
+            return self.sm.delete(deployment, load_relationships=False)
 
     def _reset_operations(self, execution, from_states=None):
         """Force-resume the execution: restart failed operations.
