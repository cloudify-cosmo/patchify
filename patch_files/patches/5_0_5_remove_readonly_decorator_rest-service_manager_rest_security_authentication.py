diff --git a/rest-service/manager_rest/security/authentication.py b/rest-service/manager_rest/security/authentication.py
index c2b1446..c152c98 100644
--- a/rest-service/manager_rest/security/authentication.py
+++ b/rest-service/manager_rest/security/authentication.py
@@ -57,7 +57,7 @@ class Authentication(object):
         user.failed_logins_counter += 1
         user_datastore.commit()
 
-    def authenticate(self, request, readonly=False):
+    def authenticate(self, request):
         user = self._internal_auth(request)
         is_bootstrap_admin = user and user.is_bootstrap_admin
         if self.external_auth_configured \
@@ -78,7 +78,6 @@ class Authentication(object):
             # (User + Password), otherwise the counter will be reset on
             # every UI refresh (every 4 sec) and accounts won't be locked.
             user.failed_logins_counter = 0
-        if not readonly:
             user.last_login_at = datetime.now()
         user_datastore.commit()
         return user
