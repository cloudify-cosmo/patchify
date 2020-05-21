diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 32f994e..73c2b5e 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -1426,6 +1426,17 @@ class ResourceManager(object):
                     'started deployment modifications: {0}'
                     .format(active_modifications))
 
+        # We need to store the pre-modification state here so that it can be
+        # used to roll back correctly on error.
+        # We have to deepcopy it because it contains a lot of mutable children
+        # which will then (sometimes) be modified by the other methods and
+        # result in a rollback that breaks the deployment and snapshots.
+        pre_modification = [
+            deepcopy(instance.to_dict()) for instance in
+            self.sm.list(models.NodeInstance,
+                         filters=deployment_id_filter,
+                         get_all_results=True)]
+
         nodes = [node.to_dict() for node
                  in self.sm.list(models.Node, filters=deployment_id_filter,
                                  get_all_results=True)]
@@ -1433,18 +1444,14 @@ class ResourceManager(object):
                           in self.sm.list(models.NodeInstance,
                                           filters=deployment_id_filter,
                                           get_all_results=True)]
+
         node_instances_modification = tasks.modify_deployment(
             nodes=nodes,
             previous_nodes=nodes,
             previous_node_instances=node_instances,
             modified_nodes=modified_nodes,
             scaling_groups=deployment.scaling_groups)
-
-        node_instances_modification['before_modification'] = [
-            instance.to_dict() for instance in
-            self.sm.list(models.NodeInstance,
-                         filters=deployment_id_filter,
-                         get_all_results=True)]
+        node_instances_modification['before_modification'] = pre_modification
 
         now = utils.get_formatted_timestamp()
         modification_id = str(uuid.uuid4())
