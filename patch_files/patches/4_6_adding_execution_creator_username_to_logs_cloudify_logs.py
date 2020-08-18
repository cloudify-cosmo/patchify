diff --git a/cloudify/logs.py b/cloudify/logs.py
index bd9a02f..d9083e8 100644
--- a/cloudify/logs.py
+++ b/cloudify/logs.py
@@ -24,7 +24,8 @@ from functools import wraps
 from cloudify import constants
 from cloudify import amqp_client_utils
 from cloudify import event as _event
-from cloudify.utils import is_management_environment
+from cloudify.utils import (is_management_environment, 
+                            get_execution_creator_username)
 from cloudify.exceptions import ClosedAMQPClientException
 text_type = unicode
 
@@ -275,6 +276,11 @@ def _send_event(ctx, context_type, event_type,
     additional_context = additional_context or {}
     message_context.update(additional_context)
 
+    if hasattr(ctx, 'execution_creator_username'):
+        if ctx.execution_creator_username:
+            message_context.update({'execution_creator_username':
+                                    ctx.execution_creator_username})
+
     event = {
         'event_type': event_type,
         'context': message_context,
@@ -406,8 +412,6 @@ def setup_agent_logger(log_name, log_level=None, log_dir=None,
 
     if log_dir:
         log_file = os.path.join(log_dir, '{0}.log'.format(log_name))
-        file_formatter = logging.Formatter(
-            ' %(asctime)-15s - %(name)s - %(levelname)s - %(message)s')
 
         # On the manager, we for sure have a logrotate policy.
         if is_management_environment():
@@ -434,7 +438,23 @@ def setup_agent_logger(log_name, log_level=None, log_dir=None,
                 filename=log_file, maxBytes=max_bytes,
                 backupCount=max_history)
         file_handler.setLevel(log_level)
-        file_handler.setFormatter(file_formatter)
+        file_handler.setFormatter(ExecutorNameFormatter())
 
         root_logger = logging.getLogger()
         root_logger.addHandler(file_handler)
+
+
+class ExecutorNameFormatter(logging.Formatter):
+    default_fmt = logging.Formatter(' %(asctime)-15s - %(name)s - '
+                                    '%(levelname)s - %(message)s')
+    user_fmt = logging.Formatter(' %(asctime)-15s - %(name)s - '
+                                 '%(levelname)s - %(username)s - %(message)s')
+
+    def format(self, record):
+        username = get_execution_creator_username()
+        if username:
+            record.username = username
+            return self.user_fmt.format(record)
+
+        return self.default_fmt.format(record)
+
