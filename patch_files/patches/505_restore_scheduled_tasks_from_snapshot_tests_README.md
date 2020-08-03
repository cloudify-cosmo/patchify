diff --git a/tests/README.md b/tests/README.md
index ed3106f..fe6b8bc 100644
--- a/tests/README.md
+++ b/tests/README.md
@@ -55,7 +55,7 @@ This project runs tests on a Cloudify Manager container created by [`docl`](http
 4. Inside a virtualenv, run:
 
    ```
-   $ pip install nose python-dateutil
+   $ pip install nose python-dateutil pytest
    $ pip install -e <SOURCE_ROOT>/cloudify-common
    $ pip install -e <SOURCE_ROOT>/cloudify-cli
    $ pip install -e <SOURCE_ROOT>/cloudify-manager/tests
@@ -109,7 +109,7 @@ To test everything is working as it should, run:
 
 ```
 $ cd <root directory of cloudify-manager repository>
-$ pytest -s tests/integration_tests/tests/agentless_tests/test_workflow.py:BasicWorkflowsTest.test_execute_operation
+$ pytest -s tests/integration_tests/tests/agentless_tests/test_workflow.py::BasicWorkflowsTest::test_execute_operation
 ```
 
 ### Saving the Cloudify Manager's logs
