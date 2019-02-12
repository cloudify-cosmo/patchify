diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index d63baa3..baa2bfe 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -964,7 +964,7 @@ class ResourceManager(object):
             groups=deployment_plan['groups'],
             scaling_groups=deployment_plan['scaling_groups'],
             outputs=deployment_plan['outputs'],
-            capabilities=deployment_plan['capabilities']
+            capabilities=deployment_plan.get('capabilities', {})
         )
 
     def prepare_deployment_nodes_for_storage(self,
