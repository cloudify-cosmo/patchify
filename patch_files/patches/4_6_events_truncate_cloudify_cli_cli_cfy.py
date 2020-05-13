diff --git a/cloudify_cli/cli/cfy.py b/cloudify_cli/cli/cfy.py
index e0a0876..38273d4 100644
--- a/cloudify_cli/cli/cfy.py
+++ b/cloudify_cli/cli/cfy.py
@@ -22,6 +22,8 @@ import StringIO
 import warnings
 import traceback
 from functools import wraps
+import datetime
+import re
 
 import click
 from cloudify_rest_client.constants import VisibilityState
@@ -84,6 +86,34 @@ class MutuallyExclusiveOption(click.Option):
             ctx, opts, args)
 
 
+def _parse_relative_datetime(ctx, param, rel_datetime):
+    """Change relative time (ago) to a valid timestamp"""
+    if not rel_datetime:
+        return None
+    parsed = re.findall(r"(\d+) (seconds?|minutes?|hours?|days?|weeks?"
+                        "|months?|years?) ?(ago)?",
+                        rel_datetime)
+    if not parsed or len(parsed[0]) < 2:
+        return None
+    number = int(parsed[0][0])
+    period = parsed[0][1]
+    if period[-1] != u's':
+        period += u's'
+    now = datetime.datetime.utcnow()
+    if period == u'years':
+        result = now.replace(year=now.year - number)
+    elif period == u'months':
+        if now.month > number:
+            result = now.replace(month=now.month - number)
+        else:
+            result = now.replace(month=now.month - number + 12,
+                                 year=now.year - 1)
+    else:
+        delta = datetime.timedelta(**{period: number})
+        result = now - delta
+    return result.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
+
+
 def _format_version_data(version_data,
                          prefix=None,
                          suffix=None,
@@ -1410,5 +1440,66 @@ class Options(object):
             required=True,
             help=helptexts.PLUGIN_YAML_PATH)
 
+    @staticmethod
+    def from_datetime(required=False, mutually_exclusive_with=None,
+                      help=helptexts.FROM_DATETIME):
+        kwargs = {
+            'required': required,
+            'type': str,
+            'help': help,
+        }
+        if mutually_exclusive_with:
+            kwargs['cls'] = MutuallyExclusiveOption
+            kwargs['mutually_exclusive'] = mutually_exclusive_with
+        return click.option('from_datetime', '--from', **kwargs)
+
+    @staticmethod
+    def to_datetime(required=False, mutually_exclusive_with=None,
+                    help=helptexts.TO_DATETIME):
+        kwargs = {
+            'required': required,
+            'type': str,
+            'help': help,
+        }
+        if mutually_exclusive_with:
+            kwargs['cls'] = MutuallyExclusiveOption
+            kwargs['mutually_exclusive'] = mutually_exclusive_with
+        return click.option('to_datetime', '--to', **kwargs)
+
+    @staticmethod
+    def before(required=False,
+               mutually_exclusive_with=None,
+               help=helptexts.BEFORE):
+        kwargs = {
+            'required': required,
+            'type': str,
+            'callback': _parse_relative_datetime,
+            'expose_value': True,
+            'help': help,
+        }
+        if mutually_exclusive_with:
+            kwargs['cls'] = MutuallyExclusiveOption
+            kwargs['mutually_exclusive'] = mutually_exclusive_with
+        return click.option('--before', **kwargs)
+
+    @staticmethod
+    def store_before(default=False):
+        return click.option(
+            '--store-before',
+            is_flag=True,
+            default=default,
+            help=helptexts.STORE_BEFORE_DELETION
+        )
+
+    @staticmethod
+    def store_output_path():
+        return click.option(
+            '-o',
+            '--output-path',
+            required=False,
+            type=click.Path(file_okay=True, dir_okay=False),
+            help=helptexts.STORE_OUTPUT_PATH
+        )
+
 
 options = Options()
