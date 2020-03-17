diff --git a/rest-service/manager_rest/rest/resources_v3_1/cluster_status.py b/rest-service/manager_rest/rest/resources_v3_1/cluster_status.py
index ed39840..6b4cfb8 100644
--- a/rest-service/manager_rest/rest/resources_v3_1/cluster_status.py
+++ b/rest-service/manager_rest/rest/resources_v3_1/cluster_status.py
@@ -25,7 +25,8 @@ from manager_rest.security.authorization import authorize
 from manager_rest.rest.rest_decorators import marshal_with
 from manager_rest.storage import models, get_storage_manager
 from manager_rest.security import SecuredResourceBannedSnapshotRestore
-from manager_rest.cluster_status_manager import (get_cluster_status,
+from manager_rest.cluster_status_manager import (STATUS,
+                                                 get_cluster_status,
                                                  write_status_report)
 from manager_rest.rest.rest_utils import (parse_datetime_string,
                                           verify_and_convert_bool,
@@ -59,12 +60,13 @@ class ClusterStatus(SecuredResourceBannedSnapshotRestore):
             'summary',
             request.args.get('summary', False)
         )
-
         cluster_status = get_cluster_status()
 
-        # If the response should be only the summary - mainly for LB
+        # If the response should be only the summary
         if summary_response:
-            return {'status': cluster_status['status'], 'services': {}}
+            short_status = cluster_status.get(STATUS)
+            status_code = 500 if short_status == ServiceStatus.FAIL else 200
+            return {'status': short_status, 'services': {}}, status_code
 
         return cluster_status
 
@@ -113,3 +115,4 @@ class BrokerClusterStatus(ClusterStatus):
         self._write_report(node_id,
                            models.RabbitMQBroker,
                            CloudifyNodeType.BROKER)
+
