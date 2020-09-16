diff --git a/cloudify/plugins/lifecycle.py b/cloudify/plugins/lifecycle.py
index a30aba6..58843fa 100644
--- a/cloudify/plugins/lifecycle.py
+++ b/cloudify/plugins/lifecycle.py
@@ -99,6 +99,8 @@ class LifecycleProcessor(object):
             name=self._name_prefix + 'install',
             node_instance_subgraph_func=install_node_instance_subgraph,
             graph_finisher_func=self._finish_install)
+        if workflow_ctx.resume:
+            self._update_resumed_install(graph)
         graph.execute()
 
     def uninstall(self):
@@ -109,6 +111,41 @@ class LifecycleProcessor(object):
             graph_finisher_func=self._finish_uninstall)
         graph.execute()
 
+    def _update_resumed_install(self, graph):
+        """Update a resumed install graph to cleanup first.
+
+        When an install is resumed:
+         - if we are going to re-send the create operation, send delete first
+         - if we are going to re-send the start operation, send stop first
+        """
+        install_subgraphs = _find_install_subgraphs(graph)
+        for instance in self.node_instances:
+            install_subgraph = install_subgraphs.get(instance.id)
+            if not install_subgraph:
+                continue
+
+            tasks = []
+            if instance.state in ['starting'] and _would_resend(
+                    install_subgraph, 'cloudify.interfaces.lifecycle.start'):
+                tasks += _pre_resume_stop(instance)
+            if instance.state in ['creating'] and _would_resend(
+                    install_subgraph, 'cloudify.interfaces.lifecycle.create'):
+                tasks += _pre_resume_uninstall(instance)
+            if not tasks:
+                continue
+            tasks = [
+                instance.send_event('Uninstalling prior to resuming install')
+            ] + tasks + [
+                instance.send_event('Finished uninstalling')
+            ]
+
+            uninstall_subgraph = graph.subgraph(
+                'resume_cleanup_{0}'.format(instance.id))
+            sequence = uninstall_subgraph.sequence()
+            sequence.add(*tasks)
+            ignore_subgraph_on_task_failure(uninstall_subgraph)
+            _run_subgraph_before(uninstall_subgraph, install_subgraph)
+
     @make_or_get_graph
     def _process_node_instances(self,
                                 ctx,
@@ -189,6 +226,103 @@ class LifecycleProcessor(object):
                         on_dependency_added(instance, rel, task_sequence)
 
 
+def _find_install_subgraphs(graph):
+    """In the install graph, find subgraphs that install a node instance.
+
+    Make a dict of {instance id: subgraph}, based on the subgraph name.
+    """
+    install_subgraphs = {}
+    for task in graph.tasks_iter():
+        if task.is_subgraph and task.name.startswith('install_'):
+            instance_name = task.name[len('install_'):]
+            install_subgraphs[instance_name] = task
+    return install_subgraphs
+
+
+def _would_resend(subgraph, operation):
+    """Would the subgraph send the operation again?
+
+    Find the task named by operation, and check its state.
+    """
+    found_task = None
+    for task in subgraph.tasks.values():
+        if task.task_type != 'RemoteWorkflowTask':
+            continue
+        try:
+            if task.cloudify_context['operation']['name'] == operation:
+                found_task = task
+                break
+        except KeyError:
+            pass
+    else:
+        return False
+    return found_task.get_state() == workflow_tasks.TASK_PENDING
+
+
+def _pre_resume_uninstall(instance):
+    """Run these uninstall tasks before resuming/resending a create."""
+    return _skip_nop_operations(
+        pre=instance.send_event('Deleting node instance'),
+        task=instance.execute_operation(
+            'cloudify.interfaces.lifecycle.delete'),
+        post=instance.send_event('Deleted node instance')
+    )
+
+
+def _pre_resume_stop(instance):
+    """Run these stop tasks before resuming/resending a start."""
+    if is_host_node(instance):
+        host_pre_stop = _host_pre_stop(instance)
+    else:
+        host_pre_stop = []
+
+    stop = _skip_nop_operations(
+        task=instance.execute_operation(
+            'cloudify.interfaces.lifecycle.stop'),
+        post=instance.send_event('Stopped node instance'))
+    return host_pre_stop + stop
+
+
+def _run_subgraph_before(subgraph_before, subgraph_after):
+    """Hook up dependencies so that subgraph_before runs before subgraph_after.
+
+    "before" will depend on everything that "after" depends, and "after" will
+    also depend on the "before".
+    """
+    if subgraph_before.graph is not subgraph_after.graph:
+        raise RuntimeError('{0} and {1} belog to different graphs'
+                           .format(subgraph_before, subgraph_after))
+    graph = subgraph_before.graph
+    for dependency_id in graph.graph.successors(subgraph_after.id):
+        graph.add_dependency(subgraph_before.id, graph.get_task(dependency_id))
+    graph.add_dependency(subgraph_after, subgraph_before)
+
+
+def ignore_subgraph_on_task_failure(subgraph):
+    """If the subgraph fails, just ignore it.
+
+    This is to be used in the pre-resume cleanup graphs, so that
+    the cleanup failing doesn't block the install from being resumed.
+    """
+    def _ignore_subgraph_failure(tsk):
+        workflow_ctx.logger.info('Ignoring subgraph failure in cleanup')
+        for t in tsk.tasks.values():
+            if t.get_state() == workflow_tasks.TASK_PENDING:
+                tsk.remove_task(t)
+        return workflow_tasks.HandlerResult.ignore()
+
+    def _ignore_task_failure(tsk):
+        workflow_ctx.logger.info('Ignoring task failure in cleanup')
+        return workflow_tasks.HandlerResult.ignore()
+
+    for task in subgraph.tasks.values():
+        if task.is_subgraph:
+            ignore_subgraph_on_task_failure(task)
+            task.on_failure = _ignore_subgraph_failure
+        else:
+            task.on_failure = _ignore_task_failure
+
+
 def set_send_node_event_on_error_handler(task, instance):
     def send_node_event_error_handler(tsk):
         instance.send_event('Ignoring task {0} failure'.format(tsk.name))
