diff --git a/cloudify/workflows/tasks.py b/cloudify/workflows/tasks.py
index 9373c90..7ec4f49 100644
--- a/cloudify/workflows/tasks.py
+++ b/cloudify/workflows/tasks.py
@@ -18,15 +18,20 @@ import time
 import uuid
 import Queue
 
-from cloudify import exceptions
+from cloudify import exceptions, logs
 from cloudify.workflows import api
-from cloudify.manager import get_rest_client
+from cloudify.manager import (
+    get_rest_client,
+    get_node_instance,
+    update_execution_status,
+    update_node_instance
+)
 from cloudify.constants import MGMTWORKER_QUEUE
+from cloudify.state import workflow_ctx
 from cloudify.utils import exception_to_error_cause
 # imported for backwards compat:
 from cloudify.utils import INSPECT_TIMEOUT  # noqa
 
-
 INFINITE_TOTAL_RETRIES = -1
 DEFAULT_TOTAL_RETRIES = INFINITE_TOTAL_RETRIES
 DEFAULT_RETRY_INTERVAL = 30
@@ -645,18 +650,28 @@ class LocalWorkflowTask(WorkflowTask):
 
     def dump(self):
         serialized = super(LocalWorkflowTask, self).dump()
+        if hasattr(self.local_task, 'dump'):
+            serialized_local_task = self.local_task.dump()
+        else:
+            serialized_local_task = None
         serialized['parameters']['task_kwargs'] = {
             'name': self._name,
-            'local_task': None
+            'local_task': serialized_local_task
         }
         return serialized
 
     @classmethod
     def restore(cls, ctx, graph, task_descr):
-        task = super(LocalWorkflowTask, cls).restore(ctx, graph, task_descr)
-        # TODO restoring local tasks is not supported yet
-        task.local_task = lambda *a, **kw: None
-        return task
+        local_task_descr = task_descr.parameters['task_kwargs'].get(
+            'local_task')
+        if local_task_descr:
+            local_task = _LocalTask.restore(local_task_descr)
+        else:
+            # task wasn't stored. Noqa because we do want to assign a lambda
+            # here, that is a noop.
+            local_task = lambda *a, **kw: None  # NOQA
+        task_descr.parameters['task_kwargs']['local_task'] = local_task
+        return super(LocalWorkflowTask, cls).restore(ctx, graph, task_descr)
 
     def _update_stored_state(self, state):
         # no need to store SENT - work up to it can safely be redone
@@ -940,3 +955,200 @@ class HandlerResult(object):
     @classmethod
     def ignore(cls):
         return HandlerResult(cls.HANDLER_IGNORE)
+
+
+# Local tasks implementation
+# A local task is a callable that will be passed to a LocalWorkflowTask,
+# and then executed in a separate thread (see LocalTasksProcessing). Those
+# tasks can implement .restore (classmethod) and .dump methods in order to
+# be resumable.
+# The user-facing interface for those tasks are node_instance.set_state,
+# .send_event, etc.
+
+class _LocalTask(object):
+    """Base class for local tasks, containing utilities."""
+
+    # all local task disable sending task events
+    workflow_task_config = {'send_task_events': False}
+
+    @property
+    def __name__(self):
+        # utility, also making subclasses be similar to plain functions
+        return self.__class__.__name__
+
+    # avoid calling .__subclasses__() many times
+    _subclass_cache = None
+
+    @classmethod
+    def restore(cls, task_descr):
+        """Rehydrate a _LocalTask instance from a dict description.
+
+        The dict will contain a 'task' key and possibly a 'kwargs' key.
+        Choose the appropriate subclass and return an instance of it.
+        """
+        if cls._subclass_cache is None:
+            cls._subclass_cache = {
+                subcls.__name__: subcls for subcls in cls.__subclasses__()
+            }
+        task_class = cls._subclass_cache[task_descr['task']]
+        return task_class(**task_descr.get('kwargs') or {})
+
+    # split local/remote on this level. This allows us to reuse implementation,
+    # avoiding the need for separate local/remote subclasses.
+    def __call__(self):
+        if workflow_ctx.local:
+            return self.local()
+        else:
+            return self.remote()
+
+    def local(self):
+        raise NotImplementedError('Implemented by subclasses')
+
+    def remote(self):
+        raise NotImplementedError('Implemented by subclasses')
+
+    @property
+    def storage(self):
+        """Shorthand for accessing the local storage.
+
+        Only available in local workflows.
+        """
+        return workflow_ctx.internal.handler.storage
+
+
+class _SetNodeInstanceStateTask(_LocalTask):
+    """A local task that sets a node instance state."""
+
+    def __init__(self, node_instance_id, state):
+        self._node_instance_id = node_instance_id
+        self._state = state
+
+    def dump(self):
+        return {
+            'task': self.__name__,
+            'kwargs': {
+                'node_instance_id': self._node_instance_id,
+                'state': self._state
+            }
+        }
+
+    def remote(self):
+        node_instance = get_node_instance(self._node_instance_id)
+        node_instance.state = self._state
+        update_node_instance(node_instance)
+        return node_instance
+
+    def local(self):
+        self.storage.update_node_instance(
+            self._node_instance_id,
+            state=self._state,
+            version=None)
+
+
+class _GetNodeInstanceStateTask(_LocalTask):
+    """A local task that gets a node instance state."""
+
+    def __init__(self, node_instance_id):
+        self._node_instance_id = node_instance_id
+
+    def dump(self):
+        return {
+            'task': self.__name__,
+            'kwargs': {
+                'node_instance_id': self._node_instance_id
+            }
+        }
+
+    def remote(self):
+        return get_node_instance(self._node_instance_idd).state
+
+    def local(self):
+        instance = self.storage.get_node_instance(
+            self._node_instance_id)
+        return instance.state
+
+
+class _SendNodeEventTask(_LocalTask):
+    """A local task that sends a node event."""
+    def __init__(self, node_instance_id, event, additional_context):
+        self._node_instance_id = node_instance_id
+        self._event = event
+        self._additional_context = additional_context
+
+    def dump(self):
+        return {
+            'task': self.__name__,
+            'kwargs': {
+                'node_instance_id': self._node_instance_id,
+                'event': self._event,
+                'additional_context': self._additional_context
+            }
+        }
+
+    # local/remote only differ by the used output function
+    def remote(self):
+        self.send(out_func=logs.amqp_event_out)
+
+    def local(self):
+        self.send(out_func=logs.stdout_event_out)
+
+    def send(self, out_func):
+        node_instance = workflow_ctx.get_node_instance(
+            self._node_instance_id)
+        logs.send_workflow_node_event(
+            ctx=node_instance,
+            event_type='workflow_node_event',
+            message=self._event,
+            additional_context=self._additional_context,
+            out_func=out_func)
+
+
+class _SendWorkflowEventTask(_LocalTask):
+    """A local task that sends a workflow event."""
+    def __init__(self, event, event_type, args, additional_context=None):
+        self._event = event
+        self._event_type = event_type
+        self._args = args
+        self._additional_context = additional_context
+
+    def dump(self):
+        return {
+            'task': self.__name__,
+            'kwargs': {
+                'event': self._event,
+                'event_type': self.event_type,
+                'args': self._args,
+                'additional_context': self._additional_context
+            }
+        }
+
+    def __call__(self):
+        return workflow_ctx.internal.send_workflow_event(
+            event_type=self._event_type,
+            message=self._event,
+            args=self._args,
+            additional_context=self._additional_context
+        )
+
+
+class _UpdateExecutionStatusTask(_LocalTask):
+    """A local task that sets the execution status."""
+    def __init__(self, status):
+        self._status = status
+
+    def dump(self):
+        return {
+            'task': self.__class__.__name__,
+            'kwargs': {
+                'status': self._status,
+            }
+        }
+
+    def remote(self):
+        update_execution_status(
+            workflow_ctx.execution_id, self._status)
+
+    def local(self):
+        raise NotImplementedError(
+            'Update execution status is not supported for '
+            'local workflow execution')
