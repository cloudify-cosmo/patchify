diff --git a/cloudify_premium/authentication/ldap_authentication.py b/cloudify_premium/authentication/ldap_authentication.py
index d96b81a..556882f 100644
--- a/cloudify_premium/authentication/ldap_authentication.py
+++ b/cloudify_premium/authentication/ldap_authentication.py
@@ -109,9 +109,6 @@ class LdapAuthentication(AuthBase):
         new_groups = set([group.name[0].lower()
                           for group in ldap_object.groups()]) - result
         result |= new_groups
-        for group in new_groups:
-            result |= self._get_nested_groups(
-                self._ldappy.group_objects.get(group), result)
         return result
 
     def _get_cloudify_groups(self, group_names):
