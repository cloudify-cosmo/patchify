diff --git a/cloudify/logs.py b/cloudify/logs.py
index 7a1ddda..bd9a02f 100644
--- a/cloudify/logs.py
+++ b/cloudify/logs.py
@@ -26,6 +26,7 @@ from cloudify import amqp_client_utils
 from cloudify import event as _event
 from cloudify.utils import is_management_environment
 from cloudify.exceptions import ClosedAMQPClientException
+text_type = unicode
 
 EVENT_CLASS = _event.Event
 EVENT_VERBOSITY_LEVEL = _event.NO_VERBOSE
@@ -325,7 +326,7 @@ def create_event_message_prefix(event):
     event_obj = EVENT_CLASS(event, verbosity_level=EVENT_VERBOSITY_LEVEL)
     if not event_obj.has_output:
         return None
-    return str(event_obj)
+    return text_type(event_obj)
 
 
 def with_amqp_client(func):
