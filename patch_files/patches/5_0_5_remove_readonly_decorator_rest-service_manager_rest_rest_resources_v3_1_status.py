diff --git a/rest-service/manager_rest/rest/resources_v3_1/status.py b/rest-service/manager_rest/rest/resources_v3_1/status.py
index d89959a..4c444d1 100644
--- a/rest-service/manager_rest/rest/resources_v3_1/status.py
+++ b/rest-service/manager_rest/rest/resources_v3_1/status.py
@@ -23,9 +23,9 @@ from cloudify.cluster_status import ServiceStatus, NodeServiceStatus
 
 from manager_rest.rest import responses
 from manager_rest.utils import get_amqp_client
+from manager_rest.security import SecuredResource
 from manager_rest.security.authorization import authorize
 from manager_rest.rest.rest_decorators import marshal_with
-from manager_rest.security import SecuredResourceReadonlyMode
 from manager_rest.rest.rest_utils import verify_and_convert_bool
 from manager_rest.cluster_status_manager import get_syncthing_status
 from manager_rest.rest.resources_v1.status import (
@@ -62,7 +62,7 @@ OPTIONAL_SERVICES = {
 }
 
 
-class Status(SecuredResourceReadonlyMode):
+class Status(SecuredResource):
 
     @swagger.operation(
         responseClass=responses.Status,
