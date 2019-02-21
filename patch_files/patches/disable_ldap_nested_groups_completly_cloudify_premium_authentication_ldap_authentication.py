diff --git a/cloudify_premium/authentication/ldap_authentication.py b/cloudify_premium/authentication/ldap_authentication.py
index 556882f..3dad8e6 100644
--- a/cloudify_premium/authentication/ldap_authentication.py
+++ b/cloudify_premium/authentication/ldap_authentication.py
@@ -87,7 +87,7 @@ class LdapAuthentication(AuthBase):
         last_name = _get_optional_item('last_name')
 
         return UserData(username, first_name, last_name, email,
-                        self._get_nested_groups(ldap_user))
+                        ldap_user.groups())
 
     def _get_ldappy(self):
         domain = config.instance.ldap_domain
@@ -111,11 +111,9 @@ class LdapAuthentication(AuthBase):
         result |= new_groups
         return result
 
-    def _get_cloudify_groups(self, group_names):
+    def _get_cloudify_groups(self, ldap_groups):
         storage_manager = get_storage_manager()
-        ldap_groups = [self._ldappy.group_objects.get(group_name)
-                       for group_name in group_names]
-        ldap_dns = [group.distinguished_name[0] for group in ldap_groups]
+        ldap_dns = [group.distinguished_name for group in ldap_groups]
         return storage_manager.list(Group, filters={'ldap_dn': ldap_dns}).items
 
 
