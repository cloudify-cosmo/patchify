diff --git a/cloudify_types/cloudify_types/component/tests/test_polling.py b/cloudify_types/cloudify_types/component/tests/test_polling.py
index ab5017a80..c4e338db5 100644
--- a/cloudify_types/cloudify_types/component/tests/test_polling.py
+++ b/cloudify_types/cloudify_types/component/tests/test_polling.py
@@ -38,11 +38,10 @@ class TestPolling(ComponentTestBase):
         self.assertFalse(output)
 
     def test_poll_with_timeout_expected(self):
-        mock_timeout = .0001
+        mock_timeout = .01
         mock_interval = .0001
 
         def mock_return(*args, **kwargs):
-            del args, kwargs
             return True
 
         output = poll_with_timeout(
@@ -207,6 +206,6 @@ class TestPolling(ComponentTestBase):
 
     def test_component_logs_empty_infinity(self):
         redirect_logs(self.cfy_mock_client, 'some_execution_id')
-        self._ctx.logger.log.assert_called_with(
-            20,
-            "Returned nothing, let's get logs next time.")
+        self._ctx.logger.info.assert_called_with(
+            "Waiting for log messages (execution: %s)...",
+            "some_execution_id")
