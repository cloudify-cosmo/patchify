diff --git a/workflows/cloudify_system_workflows/snapshots/utils.py b/workflows/cloudify_system_workflows/snapshots/utils.py
index 9e0c9388c..cbc8518e2 100644
--- a/workflows/cloudify_system_workflows/snapshots/utils.py
+++ b/workflows/cloudify_system_workflows/snapshots/utils.py
@@ -21,8 +21,6 @@ import zipfile
 import subprocess
 import contextlib
 import datetime
-import dateutil.parser
-import pytz
 
 from cloudify.workflows import ctx
 from cloudify import constants, manager
@@ -454,28 +452,7 @@ def composer_db_schema_get_current_revision():
     return revision
 
 
-def parse_datetime_string(datetime_str):
-    """
-    :param datetime_str: A string representing date and time with timezone
-                        information.
-    :return: A datetime object, converted to UTC, with no timezone info.
-    """
-    # Parse the string to datetime object
-    date_with_offset = dateutil.parser.parse(datetime_str)
-
-    # Convert the date to UTC
-    try:
-        utc_date = date_with_offset.astimezone(pytz.utc)
-    except ValueError:
-        raise Exception(
-            'Date `{0}` missing timezone information, please provide'
-            ' valid date. \nExpected format: YYYYMMDDHHMM+HHMM or'
-            ' YYYYMMDDHHMM-HHMM i.e: 201801012230-0500'
-            ' (Jan-01-18 10:30pm EST)'.format(datetime_str))
-    # Date is in UTC, tzinfo is not necessary
-    return utc_date.replace(tzinfo=None)
-
-
 def is_later_than_now(datetime_str):
-    datetime_ts = parse_datetime_string(datetime_str)
-    return datetime.datetime.utcnow() < datetime_ts
+    return datetime.datetime.utcnow() < datetime.datetime.strptime(
+        datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ'
+    )
