diff --git a/cloudify_premium/manager.py b/cloudify_premium/manager.py
index 2150b11..33f3029 100644
--- a/cloudify_premium/manager.py
+++ b/cloudify_premium/manager.py
@@ -31,7 +31,6 @@ from manager_rest.cluster_status_manager import (get_report_path,
                                                  CLUSTER_STATUS_PATH)
 from manager_rest.security import (SecuredResource,
                                    premium_only,
-                                   SecuredResourceReadonlyMode,
                                    authenticate)
 
 from cloudify_premium.ha.agents import update_agents
@@ -104,7 +103,7 @@ class ManagersId(SecuredResource):
         return result
 
 
-class RabbitMQBrokersBase(SecuredResourceReadonlyMode):
+class RabbitMQBrokersBase(SecuredResource):
     @authorize('broker_manage')
     @marshal_with(models.RabbitMQBroker)
     @authenticate
