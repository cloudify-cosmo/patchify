diff --git a/script_runner/tasks.py b/script_runner/tasks.py
index e5cc927..91b70ed 100644
--- a/script_runner/tasks.py
+++ b/script_runner/tasks.py
@@ -414,7 +414,8 @@ class OutputConsumer(object):
 
     def consume_output(self):
         for line in self.out:
-            self.logger.info("%s%s", self.prefix, line.rstrip('\n'))
+            line = line.rstrip('\n').decode('utf-8', 'replace')
+            self.logger.info("%s%s", self.prefix, line)
         self.out.close()
 
     def join(self):
