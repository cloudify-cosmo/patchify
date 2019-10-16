diff --git a/rest-service/manager_rest/deployment_update/handlers.py b/rest-service/manager_rest/deployment_update/handlers.py
index e960752..46e3b13 100644
--- a/rest-service/manager_rest/deployment_update/handlers.py
+++ b/rest-service/manager_rest/deployment_update/handlers.py
@@ -1,9 +1,13 @@
 
 from copy import deepcopy
+from sqlalchemy import cast, and_
+from sqlalchemy.dialects.postgresql import JSON
 
 import utils as deployment_update_utils
 
 from cloudify.constants import COMPUTE_NODE_TYPE
+from cloudify.workflows import tasks as cloudify_tasks
+from cloudify.models_states import ExecutionState
 
 from manager_rest import utils
 from entity_context import get_entity_context
@@ -180,6 +184,61 @@ class OperationHandler(ModifiableEntityHandlerBase):
                 self._modify_relationship_operation,
                 self._modify_node_operation)
 
+    def _update_stored_operations(self, ctx, node, new_operation):
+        """Update the operations table with the new operation inputs."""
+
+        def _filter_operation(column):
+            # path in the parameters dict that stores the node name
+            node_name_path = ('task_kwargs', 'cloudify_context', 'node_name')
+            # ..and the operation interface name,
+            # eg. cloudify.interfaces.lifecycle.create
+            # (NOT eg. script.runner.tasks.run)
+            operation_name_path = ('task_kwargs', 'cloudify_context',
+                                   'operation', 'name')
+            # this will use postgres' json operators
+            json_column = cast(column, JSON)
+            return and_(
+                json_column[node_name_path].astext == node.id,
+                json_column[operation_name_path].astext == ctx.operation_id
+            )
+
+        executions = self.sm.list(models.Execution, filters={
+            'deployment_id': ctx.deployment_id,
+            'status': [
+                ExecutionState.PENDING,
+                ExecutionState.STARTED,
+                ExecutionState.CANCELLED,
+                ExecutionState.FAILED
+            ]
+        })
+        if not executions:
+            return
+        graphs = self.sm.list(models.TasksGraph, filters={
+            'execution_id': [e.id for e in executions]
+        })
+        if not graphs:
+            return
+        # update only those operations - for the current node, ones that
+        # in a state which can be resumed, and for the current operation
+        ops = self.sm.list(models.Operation, filters={
+            'parameters': _filter_operation,
+            '_tasks_graph_fk': [tg._storage_id for tg in graphs],
+            'state': [cloudify_tasks.TASK_RESCHEDULED,
+                      cloudify_tasks.TASK_FAILED,
+                      cloudify_tasks.TASK_PENDING]
+        })
+        new_op_inputs = new_operation['inputs']
+        for op in ops:
+            try:
+                op.parameters['task_kwargs']['kwargs'].update(new_op_inputs)
+                op.parameters['task_kwargs']['kwargs']['__cloudify_context'][
+                    'has_intrinsic_functions'] = True
+                op.parameters['task_kwargs']['cloudify_context'][
+                    'has_intrinsic_functions'] = True
+            except KeyError:
+                continue
+            self.sm.update(op, modified_attrs=['parameters'])
+
     def _modify_node_operation(self, ctx, current_entities):
         new_operation = deployment_update_utils.create_dict(
             ctx.modification_breadcrumbs, ctx.raw_entity_value)
@@ -188,6 +247,7 @@ class OperationHandler(ModifiableEntityHandlerBase):
         operations.update({ctx.operation_id: new_operation})
         node.operations = operations
         node.plugins = ctx.raw_node[ctx.PLUGINS]
+        self._update_stored_operations(ctx, node, new_operation)
         self.sm.update(node)
 
         current_node = current_entities[ctx.raw_node_id]
@@ -224,6 +284,10 @@ class OperationHandler(ModifiableEntityHandlerBase):
         node.relationships = deepcopy(relationships)
         node.plugins = ctx.raw_node[ctx.PLUGINS]
         self.sm.update(node)
+        if ctx.operations_key == 'target_operations':
+            node = get_node(ctx.deployment_id,
+                            ctx.storage_relationship['target_id'])
+        self._update_stored_operations(ctx, node, ctx.raw_entity_value)
         return ctx.entity_id
 
     def remove(self, ctx, current_entities):
