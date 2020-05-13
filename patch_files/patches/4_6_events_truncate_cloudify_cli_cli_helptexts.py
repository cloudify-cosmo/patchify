diff --git a/cloudify_cli/cli/helptexts.py b/cloudify_cli/cli/helptexts.py
index a846c89..537f12c 100644
--- a/cloudify_cli/cli/helptexts.py
+++ b/cloudify_cli/cli/helptexts.py
@@ -318,3 +318,10 @@ WAIT_AFTER_FAIL = 'When a task fails, wait this many seconds for ' \
                   'already-running tasks to return'
 RESET_OPERATIONS = 'Reset operations in started state, so that they are '\
                    'ran again unconditionally'
+
+FROM_DATETIME = "Beginning of a period"
+TO_DATETIME = "End of a period"
+BEFORE = "How long ago did the specified period ended"
+
+STORE_BEFORE_DELETION = "List and store events before deleting them"
+STORE_OUTPUT_PATH = "Store listed events to a specified file (cli side)"
