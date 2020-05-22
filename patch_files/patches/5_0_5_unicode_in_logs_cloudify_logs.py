diff --git a/cloudify/logs.py b/cloudify/logs.py
index 55333f1..c576ff4 100644
--- a/cloudify/logs.py
+++ b/cloudify/logs.py
@@ -30,6 +30,7 @@ from cloudify.utils import (is_management_environment,
                             ENV_AGENT_LOG_MAX_BYTES,
                             ENV_AGENT_LOG_MAX_HISTORY)
 from cloudify.exceptions import ClosedAMQPClientException
+from cloudify._compat import text_type
 
 EVENT_CLASS = _event.Event
 EVENT_VERBOSITY_LEVEL = _event.NO_VERBOSE
@@ -346,7 +347,7 @@ def create_event_message_prefix(event):
     event_obj = EVENT_CLASS(event, verbosity_level=EVENT_VERBOSITY_LEVEL)
     if not event_obj.has_output:
         return None
-    return str(event_obj)
+    return text_type(event_obj)
 
 
 def with_amqp_client(func):
