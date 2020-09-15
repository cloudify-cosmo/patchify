diff --git a/rest-service/manager_rest/storage/relationships.py b/rest-service/manager_rest/storage/relationships.py
index 5ed3975..4115df7 100644
--- a/rest-service/manager_rest/storage/relationships.py
+++ b/rest-service/manager_rest/storage/relationships.py
@@ -40,7 +40,9 @@ def one_to_many_relationship(child_class,
                              foreign_key_column,
                              parent_class_primary_key='_storage_id',
                              backreference=None,
-                             cascade='all'):
+                             cascade='all',
+                             backref_kwargs=None,
+                             relationship_kwargs=None):
     """Return a one-to-many SQL relationship object
     Meant to be used from inside the *child* object
 
@@ -51,6 +53,10 @@ def one_to_many_relationship(child_class,
     :param backreference: The name to give to the reference to the child
     :param cascade: in what cases to cascade changes from parent to child
     """
+    if backref_kwargs is None:
+        backref_kwargs = {}
+    if relationship_kwargs is None:
+        relationship_kwargs = {}
     backreference = backreference or child_class.__tablename__
     parent_primary_key = getattr(parent_class, parent_class_primary_key)
     return db.relationship(
@@ -58,7 +64,8 @@ def one_to_many_relationship(child_class,
         primaryjoin=lambda: parent_primary_key == foreign_key_column,
         # The following line makes sure that when the *parent* is
         # deleted, all its connected children are deleted as well
-        backref=db.backref(backreference, cascade=cascade)
+        backref=db.backref(backreference, cascade=cascade, **backref_kwargs),
+        **relationship_kwargs
     )
 
 
