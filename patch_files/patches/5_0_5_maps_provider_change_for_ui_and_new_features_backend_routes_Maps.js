diff --git a/backend/routes/Maps.js b/backend/routes/Maps.js
new file mode 100644
index 0000000..686c99e
--- /dev/null
+++ b/backend/routes/Maps.js
@@ -0,0 +1,27 @@
+const _ = require('lodash');
+const express = require('express');
+const passport = require('passport');
+const request = require('request');
+
+const config = require('../config').get();
+const logger = require('../handler/LoggerHandler').getLogger('Maps');
+
+const router = express.Router();
+router.use(passport.authenticate('cookie', { session: false }));
+
+router.get('/:z/:x/:y/:r?', (req, res) => {
+    const { x, y, z, r = '' } = req.params;
+    const { accessToken, tilesUrlTemplate } = config.app.maps;
+    const url = _.template(tilesUrlTemplate)({ x, y, z, r, accessToken });
+
+    logger.error(`Fetching map tiles from ${tilesUrlTemplate}, x=${x}, y=${y}, z=${z}, r='${r}'.`);
+    req.pipe(
+        request(url).on('error', err => {
+            const message = 'Cannot fetch map tiles.';
+            logger.error(message, err);
+            res.status(500).send({ message });
+        })
+    ).pipe(res);
+});
+
+module.exports = router;
