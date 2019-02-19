diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 596c48722..064fcee52 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -383,7 +383,8 @@ class ResourceManager(object):
         self.validate_modification_permitted(blueprint)
 
         if not force:
-            imported_blueprints_list = [b.plan[constants.IMPORTED_BLUEPRINTS]
+            imported_blueprints_list = [b.plan.get(
+                                        constants.IMPORTED_BLUEPRINTS, [])
                                         for b in self.sm.list(
                                         models.Blueprint,
                                         include=['id', 'plan'],
