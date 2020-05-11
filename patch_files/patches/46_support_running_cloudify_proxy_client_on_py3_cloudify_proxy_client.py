diff --git a/cloudify/proxy/client.py b/cloudify/proxy/client.py
index 1a93073..19cb679 100644
--- a/cloudify/proxy/client.py
+++ b/cloudify/proxy/client.py
@@ -1,4 +1,3 @@
-#!/usr/bin/env python
 #########
 # Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
 #
@@ -15,12 +14,18 @@
 #  * limitations under the License.
 
 import os
-import urllib2
 import json
 import argparse
 import sys
 
 
+try:
+    from urllib.request import urlopen
+except ImportError:
+    # py2
+    from urllib2 import urlopen
+
+
 # Environment variable for the socket url
 # (used by clients to locate the socket [http, zmq(unix, tcp)])
 CTX_SOCKET_URL = 'CTX_SOCKET_URL'
@@ -60,9 +65,8 @@ def zmq_client_req(socket_url, request, timeout):
 
 
 def http_client_req(socket_url, request, timeout):
-    response = urllib2.urlopen(socket_url,
-                               data=json.dumps(request),
-                               timeout=timeout)
+    response = urlopen(
+        socket_url, data=json.dumps(request).encode('utf-8'), timeout=timeout)
     if response.code != 200:
         raise RuntimeError('Request failed: {0}'.format(response))
     return json.loads(response.read())
@@ -137,3 +141,4 @@ def main(args=None):
 
 if __name__ == '__main__':
     main()
+
