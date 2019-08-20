diff --git a/cloudify_types/cloudify_types/component/tests/base_test_suite.py b/cloudify_types/cloudify_types/component/tests/base_test_suite.py
index 30dea27c0..2f67e5363 100644
--- a/cloudify_types/cloudify_types/component/tests/base_test_suite.py
+++ b/cloudify_types/cloudify_types/component/tests/base_test_suite.py
@@ -48,6 +48,7 @@ class ComponentTestBase(testtools.TestCase):
         super(ComponentTestBase, self).setUp()
         self._ctx = self.get_mock_ctx('test', COMPONENT_PROPS)
         self._ctx.logger.log = mock.MagicMock(return_value=None)
+        self._ctx.logger.info = mock.MagicMock(return_value=None)
         current_ctx.set(self._ctx)
         self.cfy_mock_client = MockCloudifyRestClient()
 
