diff --git a/resources/rest-service/cloudify/migrations/versions/1fbd6bf39e84_4_5_to_4_5_5.py b/resources/rest-service/cloudify/migrations/versions/1fbd6bf39e84_4_5_to_4_5_5.py
index c3d1aa8..54aa087 100644
--- a/resources/rest-service/cloudify/migrations/versions/1fbd6bf39e84_4_5_to_4_5_5.py
+++ b/resources/rest-service/cloudify/migrations/versions/1fbd6bf39e84_4_5_to_4_5_5.py
@@ -30,6 +30,18 @@ resource_tables = ['blueprints', 'plugins', 'secrets', 'snapshots', 'events',
 
 
 def upgrade():
+    # In snapshots < 4.5.5  failed_logins_counter may be null, from 4.5.5
+    # we want to make sure all null values will be replaced with zeros.
+    op.execute("""
+      UPDATE users
+      SET failed_logins_counter = 0
+      WHERE failed_logins_counter IS NULL;
+    """)
+
+    # Return the null constraint to the `failed_logins_counter` column.
+    op.alter_column('users',
+                    'failed_logins_counter',
+                    nullable=False)
     # server_default accepts string or SQL element only
     op.add_column('executions', sa.Column('is_dry_run',
                                           sa.Boolean(),
@@ -179,6 +191,11 @@ def upgrade():
 
 
 def downgrade():
+    # Temporary remove the null constraint from `failed_logins_counter`,
+    # so that restoring old snapshots with null values won't fail.
+    op.alter_column('users',
+                    'failed_logins_counter',
+                    nullable=True)
     op.drop_index(op.f('operations_id_idx'), table_name='operations')
     op.drop_index(op.f('operations_created_at_idx'), table_name='operations')
     op.drop_index(op.f('operations__tenant_id_idx'), table_name='operations')
