diff --git a/workflows/cloudify_system_workflows/deployment_environment.py b/workflows/cloudify_system_workflows/deployment_environment.py
index 747b941..589c09d 100644
--- a/workflows/cloudify_system_workflows/deployment_environment.py
+++ b/workflows/cloudify_system_workflows/deployment_environment.py
@@ -13,7 +13,6 @@
 #    * See the License for the specific language governing permissions and
 #    * limitations under the License.
 
-import glob
 import os
 import shutil
 import errno
@@ -133,7 +132,6 @@ def delete(ctx,
 
     graph.execute()
     _delete_deployment_workdir(ctx)
-    _delete_logs(ctx)
     _send_request_to_delete_deployment_from_db(ctx)
 
 
@@ -144,35 +142,6 @@ def _send_request_to_delete_deployment_from_db(ctx):
                               delete_db_mode=True)
 
 
-def _delete_logs(ctx):
-    log_dir = os.environ.get('AGENT_LOG_DIR')
-    if log_dir:
-        log_file_path = os.path.join(log_dir, 'logs',
-                                     '{0}.log'.format(ctx.deployment.id))
-        if os.path.exists(log_file_path):
-            try:
-                with open(log_file_path, 'w') as f:
-                    # Truncating instead of deleting because the logging
-                    # server currently holds a file descriptor open to this
-                    # file. If we delete the file, the logs for new
-                    # deployments that get created with the same deployment
-                    # id, will get written to a stale file descriptor and
-                    # will essentially be lost.
-                    f.truncate()
-            except IOError:
-                ctx.logger.warn(
-                    'Failed truncating {0}.'.format(log_file_path,
-                                                    exc_info=True))
-        for rotated_log_file_path in glob.glob('{0}.*'.format(
-                log_file_path)):
-            try:
-                os.remove(rotated_log_file_path)
-            except IOError:
-                ctx.logger.exception(
-                    'Failed removing rotated log file {0}.'.format(
-                        rotated_log_file_path, exc_info=True))
-
-
 def _ignore_task_on_fail_and_send_event(task, ctx):
     def failure_handler(tsk):
         ctx.send_event('Ignoring task {0} failure'.format(tsk.name))
