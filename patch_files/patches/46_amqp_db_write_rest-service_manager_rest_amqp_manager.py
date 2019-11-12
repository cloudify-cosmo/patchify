diff --git a/rest-service/manager_rest/amqp_manager.py b/rest-service/manager_rest/amqp_manager.py
index 1cde5cd..b7c8904 100644
--- a/rest-service/manager_rest/amqp_manager.py
+++ b/rest-service/manager_rest/amqp_manager.py
@@ -81,12 +81,16 @@ class AMQPManager(object):
 
         return tenant
 
-    def create_agent_user(self, agent):
+    def create_agent_user(self, agent, create_missing_agents=True):
         """
         Create a new RabbitMQ user, and grant the user permissions
         :param agent: An SQLAlchemy Agent object
         :return: The updated agent object
         """
+        if not agent.rabbitmq_username or not agent.rabbitmq_password:
+            if not create_missing_agents:
+                return agent
+
         username, encrypted_password = self._create_rabbitmq_user(agent)
         self._set_agent_rabbitmq_user_permissions(username,
                                                   agent.rabbitmq_exchange,
@@ -95,14 +99,18 @@ class AMQPManager(object):
         agent.rabbitmq_password = encrypted_password
         return agent
 
-    def sync_metadata(self):
-        """Synchronize database tenants with rabbitmq metadata"""
+    def sync_metadata(self, create_missing_agents=True):
+        """Synchronize database tenants with rabbitmq metadata
+
+        :param create_missing_agents: Whether to create amqp users for agents
+        """
 
         tenants = self._storage_manager.list(Tenant, get_all_results=True)
         agents = self._storage_manager.list(Agent, get_all_results=True)
         self._clear_extra_vhosts(tenants)
         self._clear_extra_users(tenants, agents)
-        self._add_missing_vhosts_and_users(tenants, agents)
+        self._add_missing_vhosts_and_users(
+            tenants, agents, create_missing_agents=create_missing_agents)
 
     def _create_rabbitmq_user(self, resource):
         username = resource.rabbitmq_username or \
@@ -118,17 +126,21 @@ class AMQPManager(object):
         self._client.create_user(username, password)
         return username, encrypted_password
 
-    def _add_missing_vhosts_and_users(self, tenants, agents):
+    def _add_missing_vhosts_and_users(self, tenants, agents,
+                                      create_missing_agents=True):
         """Create vhosts and users present in the database"""
 
         for tenant in tenants:
             updated_tenant = self.create_tenant_vhost_and_user(tenant)
-            self._storage_manager.update(updated_tenant)
+            if create_missing_agents:
+                self._storage_manager.update(updated_tenant)
 
         for agent in agents:
             if agent.state != AgentState.RESTORED:
-                updated_agent = self.create_agent_user(agent)
-                self._storage_manager.update(updated_agent)
+                updated_agent = self.create_agent_user(
+                    agent, create_missing_agents=create_missing_agents)
+                if create_missing_agents:
+                    self._storage_manager.update(updated_agent)
 
     def _clear_extra_vhosts(self, tenants):
         """Remove vhosts in rabbitmq not present in the database"""
