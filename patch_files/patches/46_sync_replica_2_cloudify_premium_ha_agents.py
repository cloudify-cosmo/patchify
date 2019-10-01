diff --git a/cloudify_premium/ha/agents.py b/cloudify_premium/ha/agents.py
index 0699f78..ac98955 100644
--- a/cloudify_premium/ha/agents.py
+++ b/cloudify_premium/ha/agents.py
@@ -17,8 +17,9 @@ from __future__ import absolute_import
 
 import json
 import logging
-
 from collections import namedtuple
+
+import pika
 from sqlalchemy.orm.attributes import flag_modified
 
 from cloudify import amqp_client
@@ -78,7 +79,8 @@ class AgentsController(object):
         try:
             with utils.get_storage_manager() as sm:
                 self.broadcast_task(sm, task)
-        except amqp_client.ConnectionTimeoutError:
+        except (amqp_client.ConnectionTimeoutError,
+                pika.exceptions.ConnectionClosed):
             # connection refused - rabbitmq is not running, so there's no
             # agents to update
             return
