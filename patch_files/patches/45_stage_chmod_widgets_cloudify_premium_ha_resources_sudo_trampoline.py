diff --git a/cloudify_premium/ha/resources/sudo_trampoline.py b/cloudify_premium/ha/resources/sudo_trampoline.py
index 57f3d2a..51642cd 100644
--- a/cloudify_premium/ha/resources/sudo_trampoline.py
+++ b/cloudify_premium/ha/resources/sudo_trampoline.py
@@ -21,6 +21,8 @@ def promote(config):
     services = config['manager_services']
     subprocess.check_call(['systemctl', 'enable'] + services)
     subprocess.check_call(['systemctl', 'start'] + services)
+    subprocess.check_call(
+        ['chmod', 'a+w', '-R', '/opt/cloudify-stage/dist/userData'])
 
 
 def follow(config, master):
@@ -28,6 +30,8 @@ def follow(config, master):
     logging.debug('disabling: {0}'.format(services))
     subprocess.check_call(['systemctl', 'stop'] + services)
     subprocess.check_call(['systemctl', 'disable'] + services)
+    subprocess.check_call(
+        ['chmod', 'a+w', '-R', '/opt/cloudify-stage/dist/userData'])
 
 
 def update_nginx(config, allow=False, location=None):
