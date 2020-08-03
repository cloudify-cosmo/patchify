diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 6c7d005..010cddb 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -27,7 +27,8 @@ from flask_security import current_user
 
 from cloudify.cryptography_utils import encrypt
 from cloudify.workflows import tasks as cloudify_tasks
-from cloudify.plugins.install_utils import INSTALLING_PREFIX
+from cloudify.plugins.install_utils import (INSTALLING_PREFIX,
+                                            remove_status_prefix)
 from cloudify.models_states import (SnapshotState,
                                     ExecutionState,
                                     VisibilityState,
@@ -280,6 +281,10 @@ class ResourceManager(object):
             self._validate_plugin_yaml(plugin)
 
         if not utils.plugin_installable_on_current_platform(plugin):
+            plugin_entry = self.sm.get(models.Plugin, plugin.id)
+            plugin_entry = remove_status_prefix(plugin_entry)
+            if plugin_entry:
+                self.sm.update(plugin_entry)
             return
 
         self._execute_system_workflow(
@@ -2243,3 +2248,4 @@ def add_to_dict_values(dictionary, key, value):
         dictionary[key].append(value)
         return
     dictionary[key] = [value]
+
