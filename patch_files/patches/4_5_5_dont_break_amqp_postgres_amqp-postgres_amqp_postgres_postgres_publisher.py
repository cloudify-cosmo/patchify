diff --git a/amqp-postgres/amqp_postgres/postgres_publisher.py b/amqp-postgres/amqp_postgres/postgres_publisher.py
index 416eaf1..7ac13eb 100644
--- a/amqp-postgres/amqp_postgres/postgres_publisher.py
+++ b/amqp-postgres/amqp_postgres/postgres_publisher.py
@@ -189,9 +189,9 @@ class DBLogEventPublisher(object):
                     self._store(conn, items)
                 except psycopg2.OperationalError as e:
                     self.on_db_connection_error(e)
-                except psycopg2.IntegrityError:
-                    logger.exception('Error storing %d logs+events',
-                                     len(items))
+                except Exception:
+                    logger.info('Error storing %d logs+events in batch',
+                                len(items))
                     conn.rollback()
                     # in case the integrityError was caused by stale cache,
                     # clean it entirely before trying to insert without
@@ -274,6 +274,18 @@ class DBLogEventPublisher(object):
             except psycopg2.IntegrityError:
                 logger.debug('Error storing %s: %s', exchange, item)
                 conn.rollback()
+            except psycopg2.ProgrammingError as e:
+                if e.pgcode == psycopg2.errorcodes.UNDEFINED_COLUMN:
+                    logger.debug('Error storing %s: %s (undefined column)',
+                                 exchange, item)
+                else:
+                    logger.exception('Error storing %s: %s (ProgrammingError)',
+                                     exchange, item)
+                conn.rollback()
+            except Exception:
+                logger.exception('Unexpected error while storing %s: %s',
+                                 exchange, item)
+                conn.rollback()
 
     def _insert_events(self, cursor, events):
         if not events:
