diff --git a/rest-service/manager_rest/test/endpoints/test_events_v2.py b/rest-service/manager_rest/test/endpoints/test_events_v2.py
index 25d8d30..1261f68 100644
--- a/rest-service/manager_rest/test/endpoints/test_events_v2.py
+++ b/rest-service/manager_rest/test/endpoints/test_events_v2.py
@@ -12,6 +12,8 @@
 #  * See the License for the specific language governing permissions and
 #  * limitations under the License.
 
+from mock import patch
+
 from manager_rest.test.attribute import attr
 
 from manager_rest.test import base_test
@@ -44,3 +46,26 @@ class EventsTest(base_test.BaseServerTestCase):
         response = self.client.events.delete(
             '<deployment_id>', include_logs=True)
         self.assertEqual(response.items, [0])
+
+    @attr(client_min_version=3,
+          client_max_version=base_test.LATEST_API_VERSION)
+    def test_delete_events_timestamp_range(self):
+        response = self.client.events.delete(
+            '<deployment_id>', include_logs=True,
+            from_datetime='2020-01-01', to_datetime='2020-02-02')
+        self.assertEqual(response.items, [0])
+
+    @attr(client_min_version=3,
+          client_max_version=base_test.LATEST_API_VERSION)
+    @patch('manager_rest.rest.resources_v2.events.Events._store_log_entries')
+    def test_delete_events_store_before(self, store_log_entries):
+        response = self.client.events.delete(
+            '<deployment_id>', include_logs=False,
+            store_before='true')
+        self.assertEqual(store_log_entries.call_count, 1)
+        self.assertEqual(response.items, [0])
+        response = self.client.events.delete(
+            '<deployment_id>', include_logs=True,
+            store_before='true')
+        self.assertEqual(store_log_entries.call_count, 3)
+        self.assertEqual(response.items, [0])
