diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 441b2f3..32f994e 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -718,7 +718,7 @@ class ResourceManager(object):
             wait_after_fail=wait_after_fail,
             scheduled_time=scheduled_time)
 
-        is_cascading_workflow = workflow.get('is_cascading', True)
+        is_cascading_workflow = workflow.get('is_cascading', False)
         if is_cascading_workflow:
             components_dep_ids = self._find_all_components_deployment_id(
                 deployment_id)
