diff --git a/rest-service/manager_rest/security/__init__.py b/rest-service/manager_rest/security/__init__.py
index 77c4288..e5c2bde 100644
--- a/rest-service/manager_rest/security/__init__.py
+++ b/rest-service/manager_rest/security/__init__.py
@@ -20,8 +20,7 @@ from .secured_resource import (  # NOQA
     MissingPremiumFeatureResource,
     premium_only,
     allow_on_community,
-    SecuredResourceReadonlyMode,
     SecuredResourceBannedSnapshotRestore,
     authenticate
 )
-from .authorization import is_user_action_allowed  # NOQA
\ No newline at end of file
+from .authorization import is_user_action_allowed  # NOQA
