diff --git a/cloudify_rest_client/operations.py b/cloudify_rest_client/operations.py
index abf1066..e1e7452 100644
--- a/cloudify_rest_client/operations.py
+++ b/cloudify_rest_client/operations.py
@@ -29,6 +29,18 @@ class Operation(dict):
     def parameters(self):
         return self.get('parameters', {})

+    @property
+    def name(self):
+        return self.get('name')
+
+    @property
+    def containing_subgraph(self):
+        return self.get('parameters', {}).get('containing_subgraph')
+
+    @property
+    def info(self):
+        return self.get('parameters', {}).get('info')
+

 class OperationsClient(object):
     def __init__(self, api):
@@ -36,8 +48,12 @@ class OperationsClient(object):
         self._uri_prefix = 'operations'
         self._wrapper_cls = Operation

-    def list(self, graph_id):
+    def list(self, graph_id, _offset=None, _size=None):
         params = {'graph_id': graph_id}
+        if _offset is not None:
+            params['_offset'] = _offset
+        if _size is not None:
+            params['_size'] = _size
         response = self.api.get('/{self._uri_prefix}'.format(self=self),
                                 params=params)
         return ListResponse(
