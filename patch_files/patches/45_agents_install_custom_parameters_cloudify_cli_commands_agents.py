diff --git a/cloudify_cli/commands/agents.py b/cloudify_cli/commands/agents.py
index da1b4d0..d787ed7 100644
--- a/cloudify_cli/commands/agents.py
+++ b/cloudify_cli/commands/agents.py
@@ -240,7 +240,8 @@ def run_worker(
         timeout = 900
         try:
             execution = client.executions.start(
-                dep_id, workflow_id, parameters)
+                dep_id, workflow_id, parameters,
+                allow_custom_parameters=True)
             execution = wait_for_execution(
                 client,
                 execution,
