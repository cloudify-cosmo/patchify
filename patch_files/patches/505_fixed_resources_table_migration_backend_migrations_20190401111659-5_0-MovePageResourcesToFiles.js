diff --git a/backend/migrations/20190401111659-5_0-MovePageResourcesToFiles.js b/backend/migrations/20190401111659-5_0-MovePageResourcesToFiles.js
index f75a53c..e0d6067 100644
--- a/backend/migrations/20190401111659-5_0-MovePageResourcesToFiles.js
+++ b/backend/migrations/20190401111659-5_0-MovePageResourcesToFiles.js
@@ -1,7 +1,6 @@
 const fs = require('fs-extra');
 const moment = require('moment');
 const path = require('path');
-const _ = require('lodash');
 
 const ResourceTypes = require('../db/types/ResourceTypes');
 const ResourcesModel = require('../db/ResourcesModel');
@@ -48,40 +47,5 @@ module.exports = {
             });
     },
 
-    down: (queryInterface, Sequelize, logger) => {
-        const pageFiles = fs
-            .readdirSync(userPagesFolder)
-            .filter(fileName => fs.lstatSync(path.resolve(userPagesFolder, fileName)).isFile());
-        logger.info(`Found ${pageFiles.length} page files: ${_.join(pageFiles, ', ')}`);
-
-        const records = [];
-        for (const pageFile of pageFiles) {
-            const pageFilePath = path.resolve(userPagesFolder, pageFile);
-            try {
-                const pageFileContent = fs.readJsonSync(pageFilePath);
-
-                records.push({
-                    resourceId: pageFile.replace('.json', ''),
-                    type: ResourceTypes.PAGE,
-                    createdAt: pageFileContent.updatedAt || new Date(),
-                    updatedAt: pageFileContent.updatedAt || new Date(),
-                    creator: pageFileContent.updatedBy || 'admin'
-                });
-
-                logger.info(`Removing unnecessary parts from file ${pageFile}.`);
-                const newPageFileContent = {
-                    name: pageFileContent.name || pageFile,
-                    widgets: pageFileContent.widgets
-                };
-                fs.writeJsonSync(pageFilePath, newPageFileContent, { spaces: 2, EOL: '\n' });
-            } catch (error) {
-                logger.error(`Cannot process ${pageFile}. Error: ${error}.`);
-            }
-        }
-
-        logger.info('Records to be inserted:', records);
-        if (!_.isEmpty(records)) {
-            return queryInterface.bulkInsert('Resources', records);
-        }
-    }
+    down: () => Promise.resolve()
 };
