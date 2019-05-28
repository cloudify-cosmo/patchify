diff --git a/rest-service/manager_rest/resource_manager.py b/rest-service/manager_rest/resource_manager.py
index 064fcee..b18d149 100644
--- a/rest-service/manager_rest/resource_manager.py
+++ b/rest-service/manager_rest/resource_manager.py
@@ -474,6 +474,8 @@ class ResourceManager(object):

         All operations that were failed are going to be retried,
         the execution itself is going to be set to pending again.
+        Operations that were retried by another operation, will
+        not be reset.

         :return: Whether to continue with running the execution
         """
@@ -487,7 +489,13 @@ class ResourceManager(object):
             operations = self.sm.list(models.Operation,
                                       filters={'tasks_graph': graph},
                                       get_all_results=True)
+            retried_operations = set(
+                op.parameters['retried_task']
+                for op in operations
+                if op.parameters.get('retried_task'))
             for operation in operations:
+                if operation.id in retried_operations:
+                    continue
                 if operation.state in (cloudify_tasks.TASK_RESCHEDULED,
                                        cloudify_tasks.TASK_FAILED):
                     operation.state = cloudify_tasks.TASK_PENDING
