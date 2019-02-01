diff --git a/cloudify_agent/installer/config/installer_config.py b/cloudify_agent/installer/config/installer_config.py
index 98db66b..a9ca3e2 100644
--- a/cloudify_agent/installer/config/installer_config.py
+++ b/cloudify_agent/installer/config/installer_config.py
@@ -61,6 +61,7 @@ def create_runner(agent_config, validate_connection):
                     uri=agent_config.get('uri'),
                     transport=agent_config.get('transport'),
                     logger=ctx.logger,
+                    tmpdir=agent_config.tmpdir,
                     validate_connection=validate_connection)
             else:
                 runner = FabricRunner(
@@ -71,6 +72,7 @@ def create_runner(agent_config, validate_connection):
                     password=agent_config.get('password'),
                     fabric_env=agent_config.get('fabric_env'),
                     logger=ctx.logger,
+                    tmpdir=agent_config.tmpdir,
                     validate_connection=validate_connection)
         except CommandExecutionError as e:
             message = e.error
