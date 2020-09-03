diff --git a/cloudify/tests/test_tasks_graph.py b/cloudify/tests/test_tasks_graph.py
index 3e3c1b6..9cbd410 100644
--- a/cloudify/tests/test_tasks_graph.py
+++ b/cloudify/tests/test_tasks_graph.py
@@ -18,6 +18,8 @@ import time
 import unittest
 from contextlib import contextmanager
 
+from cloudify_rest_client.operations import Operation
+
 from cloudify.workflows import api
 from cloudify.workflows import tasks
 from cloudify.workflows.tasks_graph import TaskDependencyGraph
@@ -187,3 +189,150 @@ class TestTasksGraphExecute(unittest.TestCase):
                 self.fail('Execution should have been cancelled')
         self.assertFalse(task.apply_async.called)
         self.assertFalse(task.cancel.called)
+
+
+class TestTaskGraphRestore(testtools.TestCase):
+    def _remote_task(self):
+        """Make a RemoteWorkflowTask mock for use in tests"""
+        return {
+            'type': 'RemoteWorkflowTask',
+            'dependencies': [],
+            'parameters': {
+                'info': {},
+                'current_retries': 0,
+                'send_task_events': False,
+                'containing_subgraph': None,
+                'task_kwargs': {
+                    'kwargs': {
+                        '__cloudify_context': {}
+                    }
+                }
+            }
+        }
+
+    def _subgraph(self):
+        """Make a SubgraphTask mock for use in tests"""
+        return {
+            'type': 'SubgraphTask',
+            'id': 0,
+            'dependencies': [],
+            'parameters': {
+                'info': {},
+                'current_retries': 0,
+                'send_task_events': False,
+                'containing_subgraph': None,
+                'task_kwargs': {}
+            }
+        }
+
+    def _restore_graph(self, operations):
+        mock_wf_ctx = mock.Mock()
+        mock_wf_ctx.get_operations.return_value = [
+            Operation(op) for op in operations]
+        mock_retrieved_graph = mock.Mock(id=0)
+        return TaskDependencyGraph.restore(mock_wf_ctx, mock_retrieved_graph)
+
+    def test_restore_empty(self):
+        """Restoring an empty list of operations results in an empty graph"""
+        graph = self._restore_graph([])
+        operations = list(graph.tasks_iter())
+        assert operations == []
+
+    def test_restore_single(self):
+        """A single operation is restored into the graph"""
+        graph = self._restore_graph([self._remote_task()])
+        operations = list(graph.tasks_iter())
+        assert len(operations) == 1
+        assert isinstance(operations[0], tasks.RemoteWorkflowTask)
+
+    def test_restore_finished(self):
+        """Finished tasks are not restored into the graph"""
+        task = self._remote_task()
+        task['state'] = tasks.TASK_SUCCEEDED
+        graph = self._restore_graph([task])
+        operations = list(graph.tasks_iter())
+        assert operations == []
+
+    def test_restore_with_subgraph(self):
+        """Restoring operations keeps subgraph structure"""
+        subgraph = self._subgraph()
+        task = self._remote_task()
+        subgraph['id'] = 15
+        task['parameters']['containing_subgraph'] = 15
+
+        graph = self._restore_graph([subgraph, task])
+        operations = list(graph.tasks_iter())
+        assert len(operations) == 2
+        subgraphs = [op for op in operations if op.is_subgraph]
+        remote_tasks = [op for op in operations if not op.is_subgraph]
+
+        assert len(subgraphs) == 1
+        assert len(remote_tasks) == 1
+
+        assert len(subgraphs[0].tasks) == 1
+        assert remote_tasks[0].containing_subgraph is subgraphs[0]
+
+    def test_restore_with_dependencies(self):
+        """Restoring operations keeps the dependency structure"""
+        task1 = self._remote_task()
+        task1['id'] = 1
+        task2 = self._remote_task()
+        task2['id'] = 2
+        task2['dependencies'] = [1]
+
+        graph = self._restore_graph([task1, task2])
+        operations = list(graph.tasks_iter())
+        assert len(operations) == 2
+        assert graph.graph.predecessors(1) == [2]
+
+    def test_restore_with_finished_subgraph(self):
+        """Restoring operations keeps subgraph structure"""
+        subgraph = self._subgraph()
+        task = self._remote_task()
+        subgraph['id'] = 15
+        task['parameters']['containing_subgraph'] = 15
+
+        subgraph['state'] = tasks.TASK_SUCCEEDED
+
+        graph = self._restore_graph([subgraph, task])
+        operations = list(graph.tasks_iter())
+        assert len(operations) == 2
+        subgraphs = [op for op in operations if op.is_subgraph]
+        remote_tasks = [op for op in operations if not op.is_subgraph]
+
+        assert len(subgraphs) == 1
+        assert len(remote_tasks) == 1
+
+        assert len(subgraphs[0].tasks) == 1
+        assert remote_tasks[0].containing_subgraph is subgraphs[0]
+
+    def test_restore_multiple_in_subgraph(self):
+        """Multiple tasks in the same subgraph, reference the same subgraph.
+
+        As opposed to restoring the same subgraph multiple times, it's all
+        references to one object. If it was restored multiple times, then
+        the next task in the subgraph would still run even if a previous
+        task failed.
+        """
+        subgraph = self._subgraph()
+        subgraph['id'] = 15
+        task1 = self._remote_task()
+        task1['id'] = 1
+        task2 = self._remote_task()
+        task2['id'] = 2
+        task1['parameters']['containing_subgraph'] = 15
+        task2['parameters']['containing_subgraph'] = 15
+
+        graph = self._restore_graph([subgraph, task1, task2])
+        operations = list(graph.tasks_iter())
+        assert len(operations) == 3
+        subgraphs = [op for op in operations if op.is_subgraph]
+        remote_tasks = [op for op in operations if not op.is_subgraph]
+
+        # those are all references to the same subgraph, the subgraph was
+        # NOT restored multiple times
+        assert remote_tasks[0].containing_subgraph \
+            is remote_tasks[1].containing_subgraph \
+            is subgraphs[0]
+
+        assert len(subgraphs[0].tasks) == 2
