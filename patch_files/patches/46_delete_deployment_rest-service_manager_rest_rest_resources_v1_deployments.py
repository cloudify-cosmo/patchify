diff --git a/rest-service/manager_rest/rest/resources_v1/deployments.py b/rest-service/manager_rest/rest/resources_v1/deployments.py
index e338018..4afc4a2 100644
--- a/rest-service/manager_rest/rest/resources_v1/deployments.py
+++ b/rest-service/manager_rest/rest/resources_v1/deployments.py
@@ -174,7 +174,9 @@ class DeploymentsId(SecuredResource):
                 deployment.id)
             if os.path.exists(deployment_folder):
                 shutil.rmtree(deployment_folder)
-        return deployment, 200
+        return {
+            'id': deployment.id
+        }, 200
 
 
 class DeploymentModifications(SecuredResource):
