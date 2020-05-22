diff --git a/cloudify/event.py b/cloudify/event.py
index 173c199..7050919 100644
--- a/cloudify/event.py
+++ b/cloudify/event.py
@@ -37,7 +37,7 @@ class Event(object):
         if info:  # spacing in between of the info and the message
             info += ' '
 
-        return '{0}  {1} {2} {3}{4}'.format(
+        return u'{0}  {1} {2} {3}{4}'.format(
             printable_timestamp,
             event_type_indicator,
             deployment_id,
@@ -77,7 +77,7 @@ class Event(object):
     def text(self):
         message = self._event['message']['text'].encode('utf-8')
         if self.is_log_message:
-            message = '{0}: {1}'.format(self.log_level, message)
+            message = u'{0}: {1}'.format(self.log_level, message)
         elif (self.event_type in ('task_rescheduled', 'task_failed')):
             causes = self._event['context'].get('task_error_causes', [])
             if causes:
@@ -90,7 +90,7 @@ class Event(object):
                         causes_out.write('{0}\n'.format('-' * 32))
                     causes_out.write(cause.get('traceback', ''))
 
-                message = '{0}\n{1}'.format(message, causes_out.getvalue())
+                message = u'{0}\n{1}'.format(message, causes_out.getvalue())
         return message
 
     @property
