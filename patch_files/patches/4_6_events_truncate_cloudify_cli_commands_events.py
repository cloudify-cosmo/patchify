diff --git a/cloudify_cli/commands/events.py b/cloudify_cli/commands/events.py
index 17668e0..bec4421 100644
--- a/cloudify_cli/commands/events.py
+++ b/cloudify_cli/commands/events.py
@@ -16,6 +16,8 @@
 
 from cloudify_rest_client.exceptions import CloudifyClientError
 
+from cloudify import logs
+
 import click
 
 from .. import utils
@@ -44,6 +46,13 @@ def events():
 @cfy.options.tail
 @cfy.options.common_options
 @cfy.options.tenant_name(required=False, resource_name_for_help='execution')
+@cfy.options.from_datetime(required=False,
+                           help="Events that occurred at this timestamp"
+                                " or after will be listed")
+@cfy.options.to_datetime(required=False,
+                         mutually_exclusive_with=['tail'],
+                         help="Events that occurred at this timestamp"
+                              " or before will be listed",)
 @cfy.options.pagination_offset
 @cfy.options.pagination_size
 @cfy.pass_client()
@@ -54,10 +63,13 @@ def list(execution_id,
          json_output,
          tail,
          tenant_name,
+         from_datetime,
+         to_datetime,
          pagination_offset,
          pagination_size,
          client,
          logger):
+    """Display events for an execution"""
     if execution_id and execution_id_opt:
         raise click.UsageError(
             "Execution ID provided both as a positional "
@@ -75,8 +87,6 @@ def list(execution_id,
                        "is now deprecated. Please provide the execution ID as "
                        "a positional argument.")
 
-    """Display events for an execution
-    """
     utils.explicit_tenant_name_message(tenant_name, logger)
     logger.info('Listing events for execution id {0} '
                 '[include_logs={1}]'.format(execution_id, include_logs))
@@ -84,7 +94,9 @@ def list(execution_id,
         execution_events = ExecutionEventsFetcher(
             client,
             execution_id,
-            include_logs=include_logs
+            include_logs=include_logs,
+            from_datetime=from_datetime,
+            to_datetime=to_datetime,
         )
 
         events_logger = get_events_logger(json_output)
@@ -94,7 +106,8 @@ def list(execution_id,
                                            client.executions.get(execution_id),
                                            events_handler=events_logger,
                                            include_logs=include_logs,
-                                           timeout=None)  # don't timeout ever
+                                           timeout=None,  # don't timeout ever
+                                           from_datetime=from_datetime)
             if execution.error:
                 logger.info('Execution of workflow {0} for deployment '
                             '{1} failed. [error={2}]'.format(
@@ -130,25 +143,102 @@ def list(execution_id,
 @cfy.options.include_logs
 @cfy.options.common_options
 @cfy.options.tenant_name(required=False, resource_name_for_help='deployment')
+@cfy.options.from_datetime(required=False,
+                           help="Events that occurred at this timestamp"
+                                " or after will be deleted")
+@cfy.options.to_datetime(required=False,
+                         mutually_exclusive_with=['before'],
+                         help="Events that occurred at this timestamp"
+                              " or before will be deleted")
+@cfy.options.before(required=False,
+                    mutually_exclusive_with=['to_datetime'],
+                    help="Events that occurred this long ago or earlier"
+                         "will be deleted")
+@cfy.options.store_before()
+@cfy.options.store_output_path()
 @cfy.pass_client()
 @cfy.pass_logger
-def delete(deployment_id, include_logs, logger, client, tenant_name):
+def delete(deployment_id, include_logs, logger, client, tenant_name,
+           from_datetime, to_datetime, before, store_before, output_path):
     """Delete events attached to a deployment
 
-    `EXECUTION_ID` is the execution events to delete.
+    `DEPLOYMENT_ID` is the deployment_id of the executions from which
+    events/logs are deleted.
     """
     utils.explicit_tenant_name_message(tenant_name, logger)
+    if before:
+        to_datetime = before
+    filter_info = {'include_logs': u'{0}'.format(include_logs)}
+    if from_datetime:
+        filter_info['from_datetime'] = u'{0}'.format(from_datetime)
+    if to_datetime:
+        filter_info['to_datetime'] = u'{0}'.format(to_datetime)
     logger.info(
-        'Deleting events for deployment id {0} [include_logs={1}]'.format(
-            deployment_id, include_logs))
+        'Deleting events for deployment id {0} [{1}]'.format(
+            deployment_id,
+            u', '.join([u'{0}={1}'.format(k, v) for k, v in
+                        filter_info.items()])))
 
     # Make sure the deployment exists - raise 404 otherwise
     client.deployments.get(deployment_id)
+
+    # List events prior to their deletion
+    if store_before and output_path:
+        exec_list = client.executions.list(deployment_id=deployment_id,
+                                           include_system_workflows=True,
+                                           _all_tenants=True)
+        with open(output_path, 'w') as output_file:
+            click.echo(
+                'Events for deployment id {0} [{1}]'.format(
+                    deployment_id,
+                    u', '.join([u'{0}={1}'.format(k, v) for k, v in
+                                filter_info.items()])),
+                file=output_file,
+                nl=True)
+            events_logger = DeletedEventsLogger(output_file)
+            for execution in exec_list:
+                execution_events = ExecutionEventsFetcher(
+                    client, execution.id, include_logs=include_logs,
+                    from_datetime=from_datetime, to_datetime=to_datetime)
+                output_file = open(output_path, 'a') if output_path else None
+                click.echo(
+                    '\nListing events for execution id {0}\n'.format(
+                        execution.id),
+                    file=output_file,
+                    nl=True)
+                total_events = execution_events.fetch_and_process_events(
+                    events_handler=events_logger.log)
+                click.echo(
+                    '\nListed {0} events'.format(total_events),
+                    file=output_file,
+                    nl=True)
+
+    # Delete events
+    delete_args = {}
+    if store_before and not output_path:
+        delete_args['store_before'] = 'true'
     deleted_events_count = client.events.delete(
-        deployment_id, include_logs=include_logs
-    )
+        deployment_id, include_logs=include_logs,
+        from_datetime=from_datetime, to_datetime=to_datetime,
+        **delete_args)
     deleted_events_count = deleted_events_count.items[0]
     if deleted_events_count:
         logger.info('\nDeleted {0} events'.format(deleted_events_count))
     else:
         logger.info('\nNo events to delete')
+
+
+class DeletedEventsLogger(object):
+    def __init__(self, output_file=None):
+        self._output_file = output_file
+
+    def log(self, events):
+        """The default events logger prints events as short messages.
+
+        :param events: The events to print.
+        :return:
+        """
+        for event in events:
+            output = logs.create_event_message_prefix(event)
+            if output:
+                click.echo(output, file=self._output_file)
