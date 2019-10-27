diff --git a/cloudify_premium/ha/consul.py b/cloudify_premium/ha/consul.py
index 01b0589..77d31f4 100644
--- a/cloudify_premium/ha/consul.py
+++ b/cloudify_premium/ha/consul.py
@@ -186,6 +186,9 @@ class ConsulHTTPClient(ConsulHTTPBase):
 
     def __init__(self, *args, **kwargs):
         cert = kwargs.pop('cert', None)
+        retries = kwargs.pop('retries', None)
+        if retries is not None:
+            self.retries = retries
         self.timeout = kwargs.pop('timeout', 3)  # seconds
         super(ConsulHTTPClient, self).__init__(*args, **kwargs)
         self.session.verify = kwargs.get('verify')
@@ -197,8 +200,9 @@ class ConsulHTTPClient(ConsulHTTPBase):
             try:
                 return method(*args, **kwargs)
             except requests.exceptions.ReadTimeout as e:
-                logger.error('{0} (retry {1}/{2})'
-                             .format(e, retry, self.retries))
+                if self.retries:
+                    logger.error('{0} (retry {1}/{2})'
+                                 .format(e, retry, self.retries))
                 exc = e
         if exc is not None:
             raise exc
@@ -231,12 +235,14 @@ class ConsulHTTPClient(ConsulHTTPBase):
 class ConsulClient(ConsulClientBase):
     def __init__(self, *args, **kwargs):
         self.timeout = kwargs.pop('timeout', 3)  # seconds
+        self.retries = kwargs.pop('retries', None)
         self.cert = kwargs.pop('cert', None)
         super(ConsulClient, self).__init__(*args, **kwargs)
 
     def connect(self, host, port, scheme, verify=True):
         return ConsulHTTPClient(host, port, scheme, verify,
-                                timeout=self.timeout, cert=self.cert)
+                                timeout=self.timeout, cert=self.cert,
+                                retries=self.retries)
 
 
 def get_consul_client(host='localhost', **kwargs):
