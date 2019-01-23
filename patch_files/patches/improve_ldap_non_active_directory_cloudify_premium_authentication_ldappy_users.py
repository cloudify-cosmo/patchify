diff --git a/cloudify_premium/authentication/ldappy/users.py b/cloudify_premium/authentication/ldappy/users.py
index 0775c13..2e24947 100644
--- a/cloudify_premium/authentication/ldappy/users.py
+++ b/cloudify_premium/authentication/ldappy/users.py
@@ -80,8 +80,12 @@ class Users(LdapQuery):
 
     @handle_ldap_connection
     def _get_by_name(self, name, attribute=None):
-        user_filter = '(|(sAMAccountName={user})(uid={user}))'.format(
-            user=name)
+        if self._ldap_config.active_directory:
+            user_filter = \
+                '(|(sAMAccountName={user})(uid={user}))'.format(user=name)
+        else:
+            user_filter = '(uid={user})'.format(user=name)
+
         search_filter = "(&{class_filter}{user_filter})".format(
             class_filter=self._class_filter, user_filter=user_filter)
         return self.search(self._base_dn,
