diff --git a/cloudify_premium/ha/watch_handlers.py b/cloudify_premium/ha/watch_handlers.py
index 3366e28..112a4f2 100644
--- a/cloudify_premium/ha/watch_handlers.py
+++ b/cloudify_premium/ha/watch_handlers.py
@@ -136,6 +136,8 @@ class WatchCommand(utils._WithConsulClient):
             @contextmanager
             def _noop():
                 yield
+            _noop.acquire = lambda *a, **kw: True
+            _noop.release = lambda *a, **kw: True
             self._lock = _noop()
         return self._lock
 
