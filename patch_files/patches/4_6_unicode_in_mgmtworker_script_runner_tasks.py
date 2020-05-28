diff --git a/script_runner/tasks.py b/script_runner/tasks.py
index 91b70ed..c55dafa 100644
--- a/script_runner/tasks.py
+++ b/script_runner/tasks.py
@@ -415,7 +415,7 @@ class OutputConsumer(object):
     def consume_output(self):
         for line in self.out:
             line = line.rstrip('\n').decode('utf-8', 'replace')
-            self.logger.info("%s%s", self.prefix, line)
+            self.logger.info(u"%s%s", self.prefix, line)
         self.out.close()
 
     def join(self):
