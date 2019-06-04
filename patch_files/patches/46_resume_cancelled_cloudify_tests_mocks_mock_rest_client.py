diff --git a/cloudify/tests/mocks/mock_rest_client.py b/cloudify/tests/mocks/mock_rest_client.py
index 8cd8216..1c2ca48 100644
--- a/cloudify/tests/mocks/mock_rest_client.py
+++ b/cloudify/tests/mocks/mock_rest_client.py
@@ -58,6 +58,10 @@ class MockRestclient(CloudifyClient):
     def agents(self):
         return MockAgentsClient()
 
+    @property
+    def operations(self):
+        return MockOperationsClient()
+
 
 class MockNodesClient(object):
 
@@ -120,3 +124,8 @@ class MockAgentsClient(object):
             'state': state,
             'create_rabbitmq_user': create_rabbitmq_user
         })
+
+
+class MockOperationsClient(object):
+    def update(self, operation_id, state):
+        pass
