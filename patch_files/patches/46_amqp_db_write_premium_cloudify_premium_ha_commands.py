diff --git a/cloudify_premium/ha/commands.py b/cloudify_premium/ha/commands.py
index ad61309..1472156 100644
--- a/cloudify_premium/ha/commands.py
+++ b/cloudify_premium/ha/commands.py
@@ -263,7 +263,7 @@ def rabbitmq_replication(logger):
         verify=instance.amqp_ca_path
     )
     logger.info('synchronizing vhost and users in rabbitmq')
-    amqp_manager.sync_metadata()
+    amqp_manager.sync_metadata(create_missing_agents=False)
 
 
 @click.command()
