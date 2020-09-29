diff --git a/backend/handler/LoggerHandler.js b/backend/handler/LoggerHandler.js
index 87960b2..5d3cd58 100644
--- a/backend/handler/LoggerHandler.js
+++ b/backend/handler/LoggerHandler.js
@@ -4,6 +4,9 @@
 
 const winston = require('winston');
 const _ = require('lodash');
+const config = require('../config').get();
+
+const { logLevel, logsFile, errorsFile } = config.app;
 
 module.exports = (function() {
     function getArgsSupportedLogger(logger) {
@@ -30,17 +33,21 @@ module.exports = (function() {
         return logger;
     }
 
-    function getLogger(category, level = 'debug') {
-        const logFormat = winston.format.printf(({ level, message, label, timestamp }) => {
-            const instanceNumber = parseInt(process.env.NODE_APP_INSTANCE);
-            return `${instanceNumber >= 0 ? `[${instanceNumber}]` : ''}[${timestamp}][${label}] ${_.upperCase(
-                level
-            )}: ${message}`;
-        });
+    function getLogger(category) {
+        const logFormat = winston.format.printf(
+            ({ level, message, label, timestamp }) => `[${timestamp}][${label}] ${_.upperCase(level)}: ${message}`
+        );
 
         const logger = winston.loggers.add(category, {
-            level,
-            transports: [new winston.transports.Console()],
+            level: logLevel,
+            transports: [
+                new winston.transports.File({ filename: logsFile }),
+                new winston.transports.File({ filename: errorsFile, level: 'error' }),
+                new winston.transports.Console({
+                    format: winston.format.colorize({ all: true })
+                })
+            ],
+
             format: winston.format.combine(
                 winston.format.label({ label: category }),
                 winston.format.timestamp(),
@@ -51,8 +58,8 @@ module.exports = (function() {
         return getArgsSupportedLogger(logger);
     }
 
-    function getStream(category, level = 'debug') {
-        const logger = getLogger(category, level);
+    function getStream(category) {
+        const logger = getLogger(category);
         return {
             write: message => logger.info(_.trim(message))
         };
