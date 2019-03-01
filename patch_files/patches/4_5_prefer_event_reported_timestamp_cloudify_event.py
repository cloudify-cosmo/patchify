diff --git a/cloudify/event.py b/cloudify/event.py
index 173c199..6d7f4ec 100644
--- a/cloudify/event.py
+++ b/cloudify/event.py
@@ -99,7 +99,9 @@ class Event(object):
 
     @property
     def timestamp(self):
-        return self._event.get('@timestamp') or self._event['timestamp']
+        return self._event.get('@timestamp') or \
+               self._event.get('reported_timestamp') or \
+               self._event['timestamp']
 
     @property
     def printable_timestamp(self):
