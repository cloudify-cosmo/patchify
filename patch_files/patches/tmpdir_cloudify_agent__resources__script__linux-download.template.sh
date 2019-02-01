diff --git a/cloudify_agent/resources/script/linux-download.sh.template b/cloudify_agent/resources/script/linux-download.sh.template
index 2e45393..3a75573 100644
--- a/cloudify_agent/resources/script/linux-download.sh.template
+++ b/cloudify_agent/resources/script/linux-download.sh.template
@@ -31,6 +31,9 @@ download()
 }
 
 # Create a temp directory and cd into it
+{% if tmpdir %}
+export TMPDIR={{ tmpdir }}
+{% endif %}
 cd $(mktemp -d)
 
 # If using `sudo` the script is running as a user, and there's no need
