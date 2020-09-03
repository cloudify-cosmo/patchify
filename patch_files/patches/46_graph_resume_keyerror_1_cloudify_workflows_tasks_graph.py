diff --git a/cloudify/workflows/tasks_graph.py b/cloudify/workflows/tasks_graph.py
index c0f86b5..f938cef 100644
--- a/cloudify/workflows/tasks_graph.py
+++ b/cloudify/workflows/tasks_graph.py
@@ -55,34 +55,9 @@ class TaskDependencyGraph(object):
     @classmethod
     def restore(cls, workflow_context, retrieved_graph):
         graph = cls(workflow_context, graph_id=retrieved_graph.id)
-        operations = workflow_context.get_operations(retrieved_graph.id)
-        ops = {}
-        ctx = workflow_context._get_current_object()
-        for op_descr in operations:
-            if op_descr.state in tasks.TERMINATED_STATES:
-                continue
-            op = OP_TYPES[op_descr.type].restore(ctx, graph, op_descr)
-            ops[op_descr.id] = op
-
-        for op in ops.values():
-            if op.containing_subgraph:
-                subgraph_id = op.containing_subgraph
-                op.containing_subgraph = None
-                subgraph = ops[subgraph_id]
-                subgraph.add_task(op)
-            else:
-                graph.add_task(op)
-
-        for op_descr in operations:
-            op = ops.get(op_descr.id)
-            if op is None:
-                continue
-            for target in op_descr.dependencies:
-                if target not in ops:
-                    continue
-                target = ops[target]
-                graph.add_dependency(op, target)
-
+        ops = workflow_context.get_operations(retrieved_graph.id)
+        graph._restore_operations(ops)
+        graph._restore_dependencies(ops)
         graph._stored = True
         return graph
 
@@ -96,6 +71,67 @@ class TaskDependencyGraph(object):
         self._stored = False
         self.id = graph_id
 
+    def _restore_dependencies(self, ops):
+        """Set dependencies between this graph's tasks according to ops.
+
+        :param ops: a list of rest-client Operation objects
+        """
+        for op_descr in ops:
+            op = self.get_task(op_descr.id)
+            if op is None:
+                continue
+            for target_id in op_descr.dependencies:
+                target = self.get_task(target_id)
+                if target is None:
+                    continue
+                self.add_dependency(op, target)
+
+    def _restore_operations(self, ops):
+        """Restore operations from ops into this graph.
+
+        :param ops: a list of rest-client Operation objects
+        """
+        ops_by_id = dict((op.id, op) for op in ops)
+        restored_ops = {}
+        for op_descr in ops:
+            if op_descr.id in restored_ops:  # already restored - a subgraph
+                continue
+            if op_descr.state in tasks.TERMINATED_STATES:
+                continue
+
+            op = self._restore_operation(op_descr)
+            restored_ops[op_descr.id] = op
+
+            # restore the subgraph - even if the subgraph was already finished,
+            # we are going to be running an operation from it, so mark it as
+            # pending again.
+            # Follow the subgraph hierarchy up.
+            while op_descr.containing_subgraph:
+                subgraph_id = op_descr.containing_subgraph
+                subgraph_descr = ops_by_id[subgraph_id]
+                subgraph_descr['state'] = tasks.TASK_STARTED
+                subgraph = self._restore_operation(subgraph_descr)
+                restored_ops[subgraph_id] = subgraph
+
+                op.containing_subgraph = subgraph
+                subgraph.add_task(op)
+
+                op, op_descr = subgraph, subgraph_descr
+
+            self.add_task(op)
+
+    def _restore_operation(self, op_descr):
+        """Create a Task object from a rest-client Operation object.
+
+        If the task was already restored before, return a reference to the
+        same object.
+        """
+        restored = self.get_task(op_descr.id)
+        if restored is not None:
+            return restored
+        return OP_TYPES[op_descr.type].restore(
+            self.ctx._get_current_object(), self, op_descr)
+
     def store(self, name):
         serialized_tasks = []
         for task in self.tasks_iter():
