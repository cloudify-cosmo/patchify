diff --git a/rest-service/manager_rest/constants.py b/rest-service/manager_rest/constants.py
index 6318ab9..c41b981 100644
--- a/rest-service/manager_rest/constants.py
+++ b/rest-service/manager_rest/constants.py
@@ -53,9 +53,8 @@ BROKER_SSL_PORT = 5671
 SECURITY_FILE_LOCATION = '/opt/manager/rest-security.conf'
 
 LOCAL_ADDRESS = '127.0.0.1'
-ALLOWED_ENDPOINTS = ['status', 'version', 'license']
-ALLOWED_MAINTENANCE_ENDPOINTS = ALLOWED_ENDPOINTS + ['maintenance',
-                                                     'snapshots']
+ALLOWED_ENDPOINTS = ['status', 'version', 'license', 'maintenance']
+ALLOWED_MAINTENANCE_ENDPOINTS = ALLOWED_ENDPOINTS + ['snapshots']
 ALLOWED_LICENSE_ENDPOINTS = ALLOWED_ENDPOINTS + ['tokens', 'config', 'cluster',
                                                  'tenants']
 CLOUDIFY_AUTH_HEADER = 'Authorization'
