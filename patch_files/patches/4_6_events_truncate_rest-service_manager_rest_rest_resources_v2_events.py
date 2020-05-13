diff --git a/rest-service/manager_rest/rest/resources_v2/events.py b/rest-service/manager_rest/rest/resources_v2/events.py
index 77ba961..dea849b 100644
--- a/rest-service/manager_rest/rest/resources_v2/events.py
+++ b/rest-service/manager_rest/rest/resources_v2/events.py
@@ -16,6 +16,9 @@
 
 from flask_restful_swagger import swagger
 from sqlalchemy import bindparam
+from datetime import datetime
+import errno
+import os
 
 from manager_rest import manager_exceptions
 from manager_rest.rest import (
@@ -34,7 +37,6 @@ from manager_rest.security.authorization import authorize
 
 
 class Events(resources_v1.Events):
-
     """Events resource.
 
     Through the events endpoint a user can retrieve both events and logs as
@@ -158,31 +160,32 @@ class Events(resources_v1.Events):
             'deployment_id': filters['deployment_id'][0],
             'tenant_id': self.current_tenant.id
         }
-
-        delete_event_query = (
-            db.session.query(Event)
-            .filter(
-                Event._execution_fk.in_(executions_query),
-                Event._tenant_id == bindparam('tenant_id')
-            )
-            .params(**params)
-        )
-        total = delete_event_query.delete(synchronize_session=False)
+        do_store_before = 'store_before' in filters and \
+                          filters['store_before'][0].upper() == 'TRUE'
+
+        delete_event_query = Events._apply_range_filters(
+            Events._build_delete_subquery(
+                Event, executions_query, params),
+            Event, range_filters)
+        if do_store_before:
+            self._store_log_entries('events', filters['deployment_id'][0],
+                                    delete_event_query.order_by(
+                                        'reported_timestamp'))
+        total = delete_event_query.delete(
+            synchronize_session=False)
 
         if 'cloudify_log' in filters['type']:
-            delete_log_query = (
-                db.session.query(Log)
-                .filter(
-                    Log._execution_fk.in_(executions_query),
-                    Log._tenant_id == bindparam('tenant_id')
-                )
-                .params(**params)
-            )
+            delete_log_query = Events._apply_range_filters(
+                Events._build_delete_subquery(
+                    Log, executions_query, params),
+                Log, range_filters)
+            if do_store_before:
+                self._store_log_entries('logs', filters['deployment_id'][0],
+                                        delete_log_query.order_by(
+                                            'reported_timestamp'))
             total += delete_log_query.delete('fetch')
 
-        metadata = {
-            'pagination': dict(pagination, total=total)
-        }
+        metadata = {'pagination': dict(pagination, total=total)}
 
         # Commit bulk row deletions to database
         db.session.commit()
@@ -190,3 +193,42 @@ class Events(resources_v1.Events):
         # We don't really want to return all of the deleted events,
         # so it's a bit of a hack to return the deleted element count.
         return ListResult([total], metadata)
+
+    @staticmethod
+    def _store_log_entries(table_name, deployment_id, select_query):
+        output_directory = Events._create_logs_output_directory()
+        output_filename = "{0}_{1}_{2}.log".format(
+            table_name, deployment_id,
+            datetime.utcnow().strftime('%Y%m%dT%H%M%S')
+        )
+        output_filename = os.path.join(output_directory, output_filename)
+        with open(output_filename, 'a') as output_file:
+            for event in select_query.all():
+                output_file.write(Events._map_event_to_log_entry(event))
+
+    @staticmethod
+    def _map_event_to_log_entry(event):
+        return '{0}  {1}\n'.format(
+            event.reported_timestamp,
+            {k: v for k, v in event.to_response().items()
+             if k != 'reported_timestamp'})
+
+    @staticmethod
+    def _create_logs_output_directory():
+        output_directory = os.path.join(os.sep, 'opt', 'manager', 'logs')
+        try:
+            os.makedirs(output_directory)
+        except OSError as ex:
+            # be happy if someone already created the path
+            if ex.errno != errno.EEXIST:
+                raise
+        return output_directory
+
+    @staticmethod
+    def _build_delete_subquery(model, execution_query, params):
+        """Build delete subquery."""
+        query = db.session.query(model).filter(
+            model._execution_fk.in_(execution_query),
+            model._tenant_id == bindparam('tenant_id'),
+        )
+        return query.params(**params)
