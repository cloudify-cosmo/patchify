diff --git a/rest-service/manager_rest/storage/resource_models.py b/rest-service/manager_rest/storage/resource_models.py
index 28a0306..439c207 100644
--- a/rest-service/manager_rest/storage/resource_models.py
+++ b/rest-service/manager_rest/storage/resource_models.py
@@ -238,7 +238,10 @@ class Execution(CreatedAtMixin, SQLResourceBase):
 
     @declared_attr
     def deployment(cls):
-        return one_to_many_relationship(cls, Deployment, cls._deployment_fk)
+        return one_to_many_relationship(
+            cls, Deployment, cls._deployment_fk,
+            backref_kwargs={'passive_deletes': True}
+        )
 
     deployment_id = association_proxy('deployment', 'id')
     blueprint_id = association_proxy('deployment', 'blueprint_id')
@@ -491,7 +494,10 @@ class Node(SQLResourceBase):
 
     @declared_attr
     def deployment(cls):
-        return one_to_many_relationship(cls, Deployment, cls._deployment_fk)
+        return one_to_many_relationship(
+            cls, Deployment, cls._deployment_fk,
+            backref_kwargs={'passive_deletes': True}
+        )
 
     deployment_id = association_proxy('deployment', 'id')
     blueprint_id = association_proxy('deployment', 'blueprint_id')
