diff --git a/backend/server.js b/backend/server.js
index 9920379..0d0066f 100644
--- a/backend/server.js
+++ b/backend/server.js
@@ -10,14 +10,13 @@ const cookieParser = require('cookie-parser');
 const morgan = require('morgan');
 const _ = require('lodash');
 
-// Initialize logger
+const config = require('./config');
+const Consts = require('./consts');
 const LoggerHandler = require('./handler/LoggerHandler');
 
+// Initialize logger
 const logger = LoggerHandler.getLogger('Server');
 
-const config = require('./config');
-const Consts = require('./consts');
-
 // Initialize the DB connection
 require('./db/Connection');
 
@@ -107,14 +106,6 @@ app.use(
     expressStaticGzip(path.resolve(__dirname, '../dist/userData'), { enableBrotli: true, indexFromEmptyFile: false })
 );
 
-// Serving static content only in development mode. In production mode it is served by Nginx.
-if (process.env.LOCAL_ENV === 'true') {
-    app.use(
-        `${contextPath}/static`,
-        expressStaticGzip(path.resolve(__dirname, '../dist/static'), { enableBrotli: true, indexFromEmptyFile: false })
-    );
-}
-
 // API Routes
 app.use(`${contextPath}/sp`, ServerProxy);
 app.use(`${contextPath}/auth`, Auth);
@@ -164,9 +155,9 @@ app.use(function(err, req, res, next) {
     res.status(err.status || 404).send({ message: message || err });
 });
 
-const startServer = instanceNumber => {
+const startServer = () => {
     app.listen(Consts.SERVER_PORT, Consts.SERVER_HOST, function() {
-        logger.info(`Server (${String(instanceNumber || 0)}) started in mode ${ServerSettings.settings.mode}`);
+        logger.info(`Server started in mode ${ServerSettings.settings.mode}`);
         if (process.env.NODE_ENV === 'development') {
             logger.info('Server started for development');
         }
@@ -174,26 +165,12 @@ const startServer = instanceNumber => {
     });
 };
 
-const instanceNumber = parseInt(process.env.NODE_APP_INSTANCE);
-if (_.isNaN(instanceNumber) || instanceNumber === 0) {
-    // Application data (widgets, templates) initialization only in the first instance
-    Promise.all([ToursHandler.init(), WidgetHandler.init(), TemplateHandler.init()])
-        .then(() => {
-            logger.info('Tours, widgets and templates data initialized successfully.');
-            startServer(instanceNumber);
-        })
-        .catch(error => {
-            logger.error(`Error during tours, widgets and templates data initialization: ${error}`);
-            process.exit(1);
-        });
-} else {
-    ToursHandler.init()
-        .then(() => {
-            logger.info('Tours data initialized successfully.');
-            startServer(instanceNumber);
-        })
-        .catch(error => {
-            logger.error(`Error during tours data initialization: ${error}`);
-            process.exit(1);
-        });
-}
+Promise.all([ToursHandler.init(), WidgetHandler.init(), TemplateHandler.init()])
+    .then(() => {
+        logger.info('Tours, widgets and templates data initialized successfully.');
+        startServer();
+    })
+    .catch(error => {
+        logger.error(`Error during tours, widgets and templates data initialization: ${error}`);
+        process.exit(1);
+    });
