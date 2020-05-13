diff --git a/cloudify_cli/execution_events_fetcher.py b/cloudify_cli/execution_events_fetcher.py
index 3eaf17a..ea77217 100644
--- a/cloudify_cli/execution_events_fetcher.py
+++ b/cloudify_cli/execution_events_fetcher.py
@@ -42,12 +42,16 @@ class ExecutionEventsFetcher(object):
                  client,
                  execution_id,
                  batch_size=100,
-                 include_logs=False):
+                 include_logs=False,
+                 from_datetime=None,
+                 to_datetime=None):
         self._client = client
         self._execution_id = execution_id
         self._batch_size = batch_size
         self._from_event = 0
         self._include_logs = include_logs
+        self._from_datetime = from_datetime
+        self._to_datetime = to_datetime
         # make sure execution exists before proceeding
         # a 404 will be raised otherwise
         self._client.executions.get(execution_id)
@@ -75,7 +79,9 @@ class ExecutionEventsFetcher(object):
             _offset=offset,
             _size=size,
             include_logs=self._include_logs,
-            sort='reported_timestamp')
+            sort='reported_timestamp',
+            from_datetime=self._from_datetime,
+            to_datetime=self._to_datetime)
         self._from_event += len(events_list_response)
         return events_list_response
 
@@ -185,7 +191,8 @@ def wait_for_execution(client,
                        events_handler=None,
                        include_logs=False,
                        timeout=900,
-                       logger=None):
+                       logger=None,
+                       from_datetime=None):
 
     # if execution already ended - return without waiting
     if execution.status in Execution.END_STATES:
@@ -196,7 +203,8 @@ def wait_for_execution(client,
 
     events_fetcher = ExecutionEventsFetcher(client,
                                             execution.id,
-                                            include_logs=include_logs)
+                                            include_logs=include_logs,
+                                            from_datetime=from_datetime)
 
     # Poll for execution status and execution logs, until execution ends
     # and we receive an event of type in WORKFLOW_END_TYPES
