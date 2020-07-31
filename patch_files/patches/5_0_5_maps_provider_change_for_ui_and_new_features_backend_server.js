diff --git a/backend/server.js b/backend/server.js
index 80bd529..9920379 100644
--- a/backend/server.js
+++ b/backend/server.js
@@ -32,21 +32,22 @@ const ServerSettings = require('./serverSettings');
 
 ServerSettings.init();
 
-const ServerProxy = require('./routes/ServerProxy');
-const UserApp = require('./routes/UserApp');
 const Applications = require('./routes/Applications');
 const BlueprintAdditions = require('./routes/BlueprintAdditions');
-const clientConfig = require('./routes/ClientConfig');
-const SourceBrowser = require('./routes/SourceBrowser');
-const GitHub = require('./routes/GitHub');
+const ClientConfig = require('./routes/ClientConfig');
 const External = require('./routes/External');
+const File = require('./routes/File');
+const GitHub = require('./routes/GitHub');
+const Maps = require('./routes/Maps');
+const Plugins = require('./routes/Plugins');
+const ServerProxy = require('./routes/ServerProxy');
+const SourceBrowser = require('./routes/SourceBrowser');
 const Style = require('./routes/Style');
-const Widgets = require('./routes/Widgets');
 const Templates = require('./routes/Templates');
 const Tours = require('./routes/Tours');
+const UserApp = require('./routes/UserApp');
 const WidgetBackend = require('./routes/WidgetBackend');
-const File = require('./routes/File');
-const Plugins = require('./routes/Plugins');
+const Widgets = require('./routes/Widgets');
 
 const ToursHandler = require('./handler/ToursHandler');
 const WidgetHandler = require('./handler/WidgetHandler');
@@ -125,7 +126,7 @@ app.use(`${contextPath}/style`, Style);
 app.use(`${contextPath}/widgets`, Widgets);
 app.use(`${contextPath}/templates`, Templates);
 app.use(`${contextPath}/tours`, Tours);
-app.use(`${contextPath}/clientConfig`, clientConfig);
+app.use(`${contextPath}/clientConfig`, ClientConfig);
 app.use(`${contextPath}/github`, GitHub);
 app.use(`${contextPath}/external`, External);
 app.use(`${contextPath}/file`, File);
@@ -134,6 +135,7 @@ app.use(`${contextPath}/config`, function(req, res) {
 });
 app.use(`${contextPath}/wb`, WidgetBackend);
 app.use(`${contextPath}/plugins`, Plugins);
+app.use(`${contextPath}/maps`, Maps);
 
 // Redirect URLs with old context path (/stage)
 app.use([oldContextPath, `${oldContextPath}/*`], function(request, response) {
