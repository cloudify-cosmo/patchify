diff --git a/cloudify_premium/ha/watch_handlers.py b/cloudify_premium/ha/watch_handlers.py
index 112a4f2..094e16e 100644
--- a/cloudify_premium/ha/watch_handlers.py
+++ b/cloudify_premium/ha/watch_handlers.py
@@ -192,11 +192,10 @@ class WatchCommand(utils._WithConsulClient):
         if not handlers:
             return
 
-        with self.lock:
-            new_index, new_value = self._run_handlers(handlers)
-            self.stored_index = new_index
-            self.stored_value = new_value
-            self.save()
+        new_index, new_value = self._run_handlers(handlers)
+        self.stored_index = new_index
+        self.stored_value = new_value
+        self.save()
 
     def _run_handlers(self, handlers, retry_interval=1):
         """Run the passed handlers, retrying as necessary.
@@ -213,22 +212,24 @@ class WatchCommand(utils._WithConsulClient):
         while handlers_to_run:
             retry += 1
             to_retry = []
-            for handler in handlers_to_run:
-                self.logger.info('{0} {1}'.format(handler.name, data))
-                try:
-                    handler(data, self.stored_value, logger=self.logger)
-                except Exception as e:
-                    if isinstance(e, utils.ConsulLockTimeoutError):
-                        self.logger.info('Timeout in {0}: {1}'
-                                         .format(handler, e))
+            with self.lock:
+                for handler in handlers_to_run:
+                    self.logger.info('{0} {1}'.format(handler.name, data))
+                    try:
+                        handler(data, self.stored_value, logger=self.logger)
+                    except Exception as e:
+                        if isinstance(e, utils.ConsulLockTimeoutError):
+                            self.logger.info('Timeout in {0}: {1}'
+                                             .format(handler, e))
+                        else:
+                            self.logger.debug('{0} error'.format(handler.name))
+                            self.logger.exception(e)
+                        # retry for the declared amount of times,
+                        # or 10 by default
+                        if retry < handler.retries:
+                            to_retry.append(handler)
                     else:
-                        self.logger.debug('{0} error'.format(handler.name))
-                        self.logger.exception(e)
-                    # retry for the declared amount of times, or 10 by default
-                    if retry < handler.retries:
-                        to_retry.append(handler)
-                else:
-                    self.logger.debug('{0} done'.format(handler.name))
+                        self.logger.debug('{0} done'.format(handler.name))
 
             handlers_to_run = to_retry
 
