diff --git a/cloudify_agent/operations.py b/cloudify_agent/operations.py
index c50b4c5..719d553 100644
--- a/cloudify_agent/operations.py
+++ b/cloudify_agent/operations.py
@@ -463,9 +463,16 @@ def create_agent_amqp(install_agent_timeout=300, manager_ip=None,
     installing the new one
     """
     old_agent = _validate_agent()
+    original_agent = copy.deepcopy(old_agent)
     update_agent_record(old_agent, AgentState.UPGRADING)
     _update_broker_config(old_agent, manager_ip, manager_certificate)
-    agents = _run_install_script(old_agent, install_agent_timeout)
+
+    try:
+        agents = _run_install_script(old_agent, install_agent_timeout)
+    except Exception as error:
+        update_agent_runtime_properties(original_agent)
+        raise error
+
     new_agent = agents['new']
     ctx.logger.info('Installed agent {0}'.format(new_agent['name']))
     create_agent_record(new_agent, AgentState.STARTING)
@@ -473,6 +480,7 @@ def create_agent_amqp(install_agent_timeout=300, manager_ip=None,
     result = _validate_current_amqp(new_agent)
     if not result['agent_alive']:
         update_agent_record(new_agent, AgentState.FAILED)
+        update_agent_runtime_properties(original_agent)
         raise RecoverableError('New agent did not start and connect')
 
     update_agent_record(new_agent, AgentState.STARTED)
