diff --git a/rest-service/manager_rest/dsl_functions.py b/rest-service/manager_rest/dsl_functions.py
index cf590bc78..693c4a516 100644
--- a/rest-service/manager_rest/dsl_functions.py
+++ b/rest-service/manager_rest/dsl_functions.py
@@ -65,6 +65,9 @@ def evaluate_deployment_capabilities(deployment_id):
     deployment = sm.get(Deployment, deployment_id, include=['capabilities'])
     methods = _get_methods(deployment_id, sm)
 
+    if not deployment.capabilities:
+        return
+
     try:
         return functions.evaluate_capabilities(
             capabilities=deployment.capabilities,
