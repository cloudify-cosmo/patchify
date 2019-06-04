diff --git a/cloudify/tests/test_dispatch.py b/cloudify/tests/test_dispatch.py
index e620eaf..9e433c6 100644
--- a/cloudify/tests/test_dispatch.py
+++ b/cloudify/tests/test_dispatch.py
@@ -38,7 +38,7 @@ class TestDispatchTaskHandler(testtools.TestCase):
     def test_handle_or_dispatch_to_subprocess(self):
         expected_result = 'the result'
         local_op_handler = self._operation(
-            func1, args=[expected_result], local=True)
+            func1, args=[expected_result])
         subprocess_op_handler = self._operation(
             func1, task_target='stub', args=[expected_result])
         for handler in [local_op_handler, subprocess_op_handler]:
@@ -299,7 +299,7 @@ class TestDispatchTaskHandler(testtools.TestCase):
             execution_env=None,
             socket_url=None,
             deployment_id=None,
-            local=False,
+            local=True,
             process_registry=None):
         module = __name__
         if not local:
@@ -309,6 +309,7 @@ class TestDispatchTaskHandler(testtools.TestCase):
         execution_env['PYTHONPATH'] = os.path.dirname(__file__)
         return dispatch.OperationHandler(cloudify_context={
             'no_ctx_kwarg': True,
+            'local': local,
             'task_id': 'test',
             'task_name': '{0}.{1}'.format(module, func.__name__),
             'task_target': task_target,
