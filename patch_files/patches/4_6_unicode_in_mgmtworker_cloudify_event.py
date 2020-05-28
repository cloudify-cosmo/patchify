diff --git a/cloudify/event.py b/cloudify/event.py
index 7050919..eaa119f 100644
--- a/cloudify/event.py
+++ b/cloudify/event.py
@@ -75,7 +75,7 @@ class Event(object):
 
     @property
     def text(self):
-        message = self._event['message']['text'].encode('utf-8')
+        message = self._event['message']['text']
         if self.is_log_message:
             message = u'{0}: {1}'.format(self.log_level, message)
         elif (self.event_type in ('task_rescheduled', 'task_failed')):
