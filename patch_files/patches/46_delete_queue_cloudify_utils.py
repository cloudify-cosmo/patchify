diff --git a/cloudify/utils.py b/cloudify/utils.py
index 1402b3e..17632a9 100644
--- a/cloudify/utils.py
+++ b/cloudify/utils.py
@@ -546,7 +546,7 @@ def is_agent_alive(name,
     :param connect: whether to connect the client (should be False if it is
                     already connected)
     """
-    handler = BlockingRequestResponseHandler(exchange=name)
+    handler = BlockingRequestResponseHandler(name)
     client.add_handler(handler)
     if connect:
         with client:
