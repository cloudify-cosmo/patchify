diff --git a/cloudify_premium/ha/fix.py b/cloudify_premium/ha/fix.py
new file mode 100644
index 0000000..3ef6223
--- /dev/null
+++ b/cloudify_premium/ha/fix.py
@@ -0,0 +1,55 @@
+########
+# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
+#
+# Licensed under the Apache License, Version 2.0 (the "License");
+# you may not use this file except in compliance with the License.
+# You may obtain a copy of the License at
+#
+#        http://www.apache.org/licenses/LICENSE-2.0
+#
+# Unless required by applicable law or agreed to in writing, software
+# distributed under the License is distributed on an "AS IS" BASIS,
+#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
+#    * See the License for the specific language governing permissions and
+#    * limitations under the License.
+
+import click
+import time
+
+
+from cloudify_premium.ha import watch_handlers
+
+
+@click.group()
+def fixup_commands():
+    pass
+
+
+@fixup_commands.command('reset-follow')
+@click.option('--force', is_flag=True, default=False)
+def reset_follow(force=False):
+    master_watch = watch_handlers.NextMasterWatch()
+    next_master_watch = watch_handlers.MasterWatchCommand()
+    master_acquired = master_watch.lock.acquire(blocking=False)
+    next_master_acquired = next_master_watch.lock.acquire(blocking=False)
+    if not force and (not master_acquired or not next_master_acquired):
+        click.echo('Unable to acquire locks - is the node currently '
+                   ' attempting to follow? Pass --force to reset anyway')
+        return
+    click.echo('Going to reset following - CTRL+C to cancel (10 seconds)')
+    time.sleep(10)
+    try:
+        master_watch.stored_value = None
+        master_watch.stored_index = None
+        master_watch.save()
+        next_master_watch.stored_value = None
+        next_master_watch.stored_index = None
+        next_master_watch.save()
+        watch_handlers.HandlerRunner().restart()
+    finally:
+        master_watch.lock.release()
+        next_master_watch.lock.release()
+
+
+if __name__ == '__main__':
+    fixup_commands()
