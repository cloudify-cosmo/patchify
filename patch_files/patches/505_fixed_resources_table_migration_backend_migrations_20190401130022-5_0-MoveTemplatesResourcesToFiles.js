diff --git a/backend/migrations/20190401130022-5_0-MoveTemplatesResourcesToFiles.js b/backend/migrations/20190401130022-5_0-MoveTemplatesResourcesToFiles.js
index 127f49b..2095093 100644
--- a/backend/migrations/20190401130022-5_0-MoveTemplatesResourcesToFiles.js
+++ b/backend/migrations/20190401130022-5_0-MoveTemplatesResourcesToFiles.js
@@ -1,7 +1,6 @@
 const fs = require('fs-extra');
 const moment = require('moment');
 const path = require('path');
-const _ = require('lodash');
 
 const ResourceTypes = require('../db/types/ResourceTypes');
 const ResourcesModel = require('../db/ResourcesModel');
@@ -54,39 +53,5 @@ module.exports = {
             });
     },
 
-    down: (queryInterface, Sequelize, logger) => {
-        const templateFiles = fs
-            .readdirSync(userTemplatesFolder)
-            .filter(fileName => fs.lstatSync(path.resolve(userTemplatesFolder, fileName)).isFile());
-        logger.info(`Found ${templateFiles.length} templates files: ${_.join(templateFiles, ', ')}`);
-
-        const records = [];
-        for (const templateFile of templateFiles) {
-            const templateFilePath = path.resolve(userTemplatesFolder, templateFile);
-            try {
-                const templateFileContent = fs.readJsonSync(templateFilePath);
-                const data = { roles: templateFileContent.roles || [], tenants: templateFileContent.tenants };
-                const { pages } = templateFileContent;
-
-                records.push({
-                    resourceId: templateFile.replace('.json', ''),
-                    type: ResourceTypes.TEMPLATE,
-                    createdAt: templateFileContent.updatedAt || new Date(),
-                    updatedAt: templateFileContent.updatedAt || new Date(),
-                    creator: templateFileContent.updatedBy || 'admin',
-                    data: JSON.stringify(data)
-                });
-
-                logger.info(`Updating file ${templateFile} with pages data:`, pages);
-                fs.writeJsonSync(templateFilePath, pages, { spaces: 2, EOL: '\n' });
-            } catch (error) {
-                logger.error(`Cannot process ${templateFile}. Error: ${error}.`);
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
