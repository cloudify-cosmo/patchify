diff --git a/rest-service/manager_rest/rest/resources_v1/executions.py b/rest-service/manager_rest/rest/resources_v1/executions.py
index 2d406fb..62333af 100644
--- a/rest-service/manager_rest/rest/resources_v1/executions.py
+++ b/rest-service/manager_rest/rest/resources_v1/executions.py
@@ -180,14 +180,16 @@ class ExecutionsId(SecuredResource):
         action = request_dict['action']
 
         valid_actions = ['cancel', 'force-cancel', 'kill', 'resume',
-                         'force-resume']
+                         'force-resume', 'requeue']
 
         if action not in valid_actions:
             raise manager_exceptions.BadParametersError(
                 'Invalid action: {0}, Valid action values are: {1}'.format(
                     action, valid_actions))
 
-        if action in ('resume', 'force-resume'):
+        if action == 'requeue':
+            return get_resource_manager().requeue_execution(execution_id)
+        elif action in ('resume', 'force-resume'):
             return get_resource_manager().resume_execution(
                 execution_id, force=action == 'force-resume')
         return get_resource_manager().cancel_execution(
