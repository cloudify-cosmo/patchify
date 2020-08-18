diff --git a/rest-service/manager_rest/workflow_executor.py b/rest-service/manager_rest/workflow_executor.py
index 2deb1e4..fabe794 100644
--- a/rest-service/manager_rest/workflow_executor.py
+++ b/rest-service/manager_rest/workflow_executor.py
@@ -179,6 +179,7 @@ def _execute_task(execution_id, execution_parameters,
     context['rest_token'] = execution_creator.get_auth_token()
     context['tenant'] = _get_tenant_dict()
     context['task_target'] = MGMTWORKER_QUEUE
+    context['execution_creator_username'] = current_user.username
     execution_parameters['__cloudify_context'] = context
     message = {
         'cloudify_task': {'kwargs': execution_parameters},
