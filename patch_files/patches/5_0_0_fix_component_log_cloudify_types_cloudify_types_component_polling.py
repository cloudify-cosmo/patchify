diff --git a/cloudify_types/cloudify_types/component/polling.py b/cloudify_types/cloudify_types/component/polling.py
index a625e9f9d..fe02868ce 100644
--- a/cloudify_types/cloudify_types/component/polling.py
+++ b/cloudify_types/cloudify_types/component/polling.py
@@ -13,6 +13,7 @@
 # limitations under the License.
 
 import time
+import logging
 
 from cloudify import ctx
 from cloudify.exceptions import NonRecoverableError
@@ -21,14 +22,6 @@ from cloudify_types.utils import handle_client_exception
 
 from .constants import POLLING_INTERVAL, PAGINATION_SIZE, EXECUTIONS_TIMEOUT
 
-PREDEFINED_LOG_LEVELS = {
-    'critical': 50,
-    'error': 40,
-    'warning': 30,
-    'info': 20,
-    'debug': 10
-}
-
 
 def poll_with_timeout(pollster,
                       timeout,
@@ -39,7 +32,7 @@ def poll_with_timeout(pollster,
     timeout = float('infinity') if timeout == -1 else timeout
     current_time = time.time()
 
-    ctx.logger.debug('Pooling with timeout {0} seconds'.format(timeout))
+    ctx.logger.debug('Pooling with timeout of {0} seconds'.format(timeout))
 
     while time.time() <= current_time + timeout:
         if pollster() != expected_result:
@@ -104,21 +97,27 @@ def redirect_logs(client, execution_id, instance_ctx=None):
                 event.get('message', "")
             )
             message = message.encode('utf-8')
+            level = event.get('level')
 
-            ctx.logger.info(
-                'Message {0} for Event {1} for execution_id {1}'.format(
-                    message, event))
+            # If the event dict had a 'level' key, then the value is
+            # a string. In that case, convert it to uppercase and get
+            # the matching Python logging constant.
+            if level:
+                level = logging.getLevelName(level.upper())
 
-            level = event.get('level')
-            if level in PREDEFINED_LOG_LEVELS:
-                ctx.logger.log(PREDEFINED_LOG_LEVELS[level], message)
-            else:
-                ctx.logger.log(20, message)
+            # In the (very) odd case that the level is still not an int
+            # (can happen if the original level value wasn't recognized
+            # by Python's logging library), then use 'INFO'.
+            if not isinstance(level, int):
+                level = logging.INFO
+
+            ctx.logger.log(level, message)
 
         last_event += len(events)
 
         if len(events) == 0:
-            ctx.logger.log(20, "Returned nothing, let's get logs next time.")
+            ctx.logger.info(
+                "Waiting for log messages (execution: %s)...", execution_id)
             break
 
     instance_ctx.runtime_properties[count_events][execution_id] = last_event
@@ -175,7 +174,7 @@ def is_deployment_execution_at_state(client,
 
     if not execution_id:
         raise NonRecoverableError(
-            'Execution id was not found for "{0}" deployment.'.format(
+            'Execution id was not found for deployment "{0}"'.format(
                 dep_id))
 
     execution_get_args = ['status', 'workflow_id',
@@ -184,20 +183,19 @@ def is_deployment_execution_at_state(client,
     execution = client.executions.get(execution_id=execution_id,
                                       _include=execution_get_args)
     ctx.logger.info(
-        'Execution "{0}" of component "{1}" state is {2}'.format(execution_id,
-                                                                 dep_id,
-                                                                 execution))
+        'Execution "%s" of component "%s" state is %s',
+        execution_id, dep_id, execution)
 
     if log_redirect:
         ctx.logger.debug(
-            'Execution info with log_redirect is {0}'.format(execution))
+            'Execution info with log_redirect is %s', execution)
         redirect_logs(client, execution_id, instance_ctx)
 
     execution_status = execution.get('status')
     if execution_status == state:
         ctx.logger.debug(
             'The status for execution'
-            ' "{0}" is {1}.'.format(execution_id, state))
+            ' "%s" is %s', execution_id, state)
 
         return True
     elif execution_status == 'failed':
@@ -226,8 +224,7 @@ def verify_execution_state(client,
         'instance_ctx': instance_ctx
     }
 
-    ctx.logger.debug('Polling execution state with: {0}'.format(
-        pollster_args))
+    ctx.logger.debug('Polling execution state with: %s', pollster_args)
     result = poll_with_timeout(
         lambda: is_deployment_execution_at_state(**pollster_args),
         timeout=timeout,
