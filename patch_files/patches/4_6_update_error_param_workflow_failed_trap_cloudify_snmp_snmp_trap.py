diff --git a/cloudify/snmp/snmp_trap.py b/cloudify/snmp/snmp_trap.py
index dfb4fe6..1e4b3dc 100644
--- a/cloudify/snmp/snmp_trap.py
+++ b/cloudify/snmp/snmp_trap.py
@@ -109,7 +109,7 @@ def _create_notification_type(event_context):
 
     if event_type == 'workflow_failed':
         error = _get_error(event_context)
-        notification_type.addVarBinds(ERROR, error)
+        notification_type.addVarBinds((ERROR, OctetString(error)))
     return notification_type
 
 
