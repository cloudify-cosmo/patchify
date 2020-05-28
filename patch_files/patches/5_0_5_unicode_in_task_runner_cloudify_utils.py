diff --git a/cloudify/utils.py b/cloudify/utils.py
index beb698a..61d326e 100644
--- a/cloudify/utils.py
+++ b/cloudify/utils.py
@@ -790,7 +790,8 @@ class OutputConsumer(object):
 
     def consume_output(self):
         for line in self.out:
-            self.logger.info("%s%s", self.prefix, line.rstrip('\n'))
+            line = line.decode('utf-8', 'replace').rstrip('\n')
+            self.logger.info(u"%s%s", self.prefix, line)
         self.out.close()
 
     def join(self):
