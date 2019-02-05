diff --git a/cloudify_agent/api/utils.py b/cloudify_agent/api/utils.py
index d4604ea..9aa4cd2 100644
--- a/cloudify_agent/api/utils.py
+++ b/cloudify_agent/api/utils.py
@@ -255,7 +255,6 @@ def render_template_to_file(template_path, file_path=None, **values):
     :param file_path: absolute path to the desired output file.
     :param values: keyword arguments passed to jinja.
     """
-
     template = get_resource(template_path)
     rendered = Template(template).render(**values)
     return content_to_file(rendered, file_path)
