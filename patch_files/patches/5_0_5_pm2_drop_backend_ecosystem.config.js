diff --git a/opt/cloudify-stage/backend/ecosystem.config.js b/ecosystem.config.js
index ce39d1b..e69de29 100644
--- a/opt/cloudify-stage/backend/ecosystem.config.js
+++ b/ecosystem.config.js
@@ -1,31 +0,0 @@
-module.exports = {
-    apps: [
-        {
-            name: 'stage-backend',
-            script: 'server.js',
-            args: process.env.STAGE_BACKEND_ARGS,
-            autorestart: true,
-            exec_mode: 'cluster',
-            instances: process.env.STAGE_BACKEND_INSTANCES,
-            max_memory_restart: '1G',
-
-            env: {
-                NODE_ENV: 'production'
-            },
-            env_development: {
-                NODE_ENV: 'development',
-                LOCAL_ENV: 'true'
-            },
-            env_production: {
-                NODE_ENV: 'production'
-            },
-            env_local_production: {
-                NODE_ENV: 'production',
-                LOCAL_ENV: 'true'
-            },
-
-            output: '/var/log/cloudify/stage/server-output.log',
-            error: '/var/log/cloudify/stage/server-errors.log'
-        }
-    ]
-};
