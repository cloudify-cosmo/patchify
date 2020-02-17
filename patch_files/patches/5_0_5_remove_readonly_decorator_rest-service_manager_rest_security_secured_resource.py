diff --git a/rest-service/manager_rest/security/secured_resource.py b/rest-service/manager_rest/security/secured_resource.py
index 0ca74d8..c0f8bda 100644
--- a/rest-service/manager_rest/security/secured_resource.py
+++ b/rest-service/manager_rest/security/secured_resource.py
@@ -28,7 +28,7 @@ from manager_rest.rest.rest_decorators import (
 from .authentication import authenticator
 
 
-def authenticate(func, readonly=False):
+def authenticate(func):
     def _extend_response_headers(response, extra_headers):
         response = jsonify(response)
         response.headers.extend(extra_headers)
@@ -51,7 +51,7 @@ def authenticate(func, readonly=False):
 
     @wraps(func)
     def wrapper(*args, **kwargs):
-        auth_response = authenticator.authenticate(request, readonly)
+        auth_response = authenticator.authenticate(request)
         auth_headers = getattr(auth_response, 'response_headers', {})
         if isinstance(auth_response, Response):
             return auth_response
@@ -75,10 +75,6 @@ def authenticate(func, readonly=False):
     return wrapper
 
 
-def authenticate_readonly_mode(func):
-    return authenticate(func, True)
-
-
 def _abort_on_premium_missing(func):
     """Mark a method as requiring premium.
 
@@ -128,15 +124,5 @@ class SecuredResourceBannedSnapshotRestore(Resource):
     method_decorators = [prevent_running_in_snapshot_restore, authenticate]
 
 
-class SecuredResourceReadonlyMode(Resource):
-    """
-    In case of readonly access to the DB with write access for the failed
-    counter login mechanism, only this kind of secured resource will allow
-    access to the endpoints needed in that scenario by not writing to a
-    readonly column.
-    """
-    method_decorators = [authenticate_readonly_mode]
-
-
 class MissingPremiumFeatureResource(Resource):
     method_decorators = [_abort_on_premium_missing]
