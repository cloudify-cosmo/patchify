diff --git a/workflows/cloudify_system_workflows/snapshots/constants.py b/workflows/cloudify_system_workflows/snapshots/constants.py
index e2245c9..6ae3336 100644
--- a/workflows/cloudify_system_workflows/snapshots/constants.py
+++ b/workflows/cloudify_system_workflows/snapshots/constants.py
@@ -49,6 +49,7 @@ COMPOSER_CONFIG_FOLDER = 'backend/conf'
 COMPOSER_BLUEPRINTS_FOLDER = 'backend/dev'
 SECURITY_FILENAME = 'rest-security.conf'
 SECURITY_FILE_LOCATION = join('/opt/manager/', SECURITY_FILENAME)
+NEW_TOKEN_FILE_NAME = 'new_token'
 
 V_4_0_0 = ManagerVersion('4.0.0')
 V_4_1_0 = ManagerVersion('4.1.0')
