diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 73c2b5e..6c7d005 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -47,6 +47,7 @@ from manager_rest.utils import (send_event,
                                 validate_deployment_and_site_visibility,
                                 extract_host_agent_plugins_from_plan)
 from manager_rest.plugins_update.constants import PLUGIN_UPDATE_WORKFLOW
+from manager_rest.rest.rest_utils import parse_datetime_string
 from manager_rest.storage import (db,
                                   get_storage_manager,
                                   models,
@@ -614,6 +615,39 @@ class ResourceManager(object):
 
         return execution
 
+    def requeue_execution(self, execution_id, force=False):
+        execution = self.sm.get(models.Execution, execution_id)
+        if execution.status != ExecutionState.SCHEDULED:
+            raise manager_exceptions.ConflictError(
+                'Cannot requeue execution: `{0}` in state: `{1}`'
+                .format(execution.id, execution.status))
+
+        workflow_id = execution.workflow_id
+        deployment = execution.deployment
+        blueprint = deployment.blueprint
+        workflow_plugins = blueprint.plan[
+            constants.WORKFLOW_PLUGINS_TO_INSTALL]
+        workflow = deployment.workflows[workflow_id]
+        execution_token = generate_execution_token(execution_id)
+
+        workflow_executor.execute_workflow(
+            workflow_id,
+            workflow,
+            workflow_plugins=workflow_plugins,
+            blueprint_id=deployment.blueprint_id,
+            deployment=deployment,
+            execution_id=execution_id,
+            execution_parameters=execution.parameters,
+            bypass_maintenance=False,
+            dry_run=False,
+            resume=False,
+            scheduled_time=parse_datetime_string(execution.scheduled_for),
+            execution_creator=execution.creator,
+            execution_token=execution_token
+        )
+
+        return execution
+
     @staticmethod
     def _set_execution_tenant(tenant_name):
         tenant = get_storage_manager().get(
