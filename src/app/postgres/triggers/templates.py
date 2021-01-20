SQL_CREATE_TRIGGER = """
    CREATE OR REPLACE FUNCTION {trigger_name}()
      RETURNS trigger AS $$
    DECLARE
      id integer;
      data json;
    BEGIN
      data = json 'null';
      IF TG_OP = 'INSERT' THEN
        id = NEW.id;
        data = row_to_json(NEW);
      ELSIF TG_OP = 'UPDATE' THEN
        id = NEW.id;
        data = json_build_object(
          'old', row_to_json(OLD),
          'new', row_to_json(NEW),
          'diff', hstore_to_json(hstore(NEW) - hstore(OLD))
        );
      ELSE
        id = OLD.id;
        data = row_to_json(OLD);
      END IF;
      PERFORM
        pg_notify(
          '{channel}',
          json_build_object(
            'table', TG_TABLE_NAME,
            'id', id,
            'type', TG_OP,
            'data', data
          )::text
        );
      RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
"""

SQL_TABLE_UPDATE = """
    DROP TRIGGER IF EXISTS
      {table_name}_notify_update ON {schema}.{table_name};
    CREATE TRIGGER {table_name}_notify_update
      AFTER UPDATE ON {schema}.{table_name}
        FOR EACH ROW
          EXECUTE PROCEDURE {trigger_name}();
"""


SQL_TABLE_INSERT = """
    DROP TRIGGER IF EXISTS
      {table_name}_notify_insert ON {schema}.{table_name};
    CREATE TRIGGER {table_name}_notify_insert
      AFTER INSERT ON {schema}.{table_name}
        FOR EACH ROW
          EXECUTE PROCEDURE {trigger_name}();
"""

SQL_TABLE_DELETE = """
    DROP TRIGGER IF EXISTS
      {table_name}_notify_delete ON {schema}.{table_name};
    CREATE TRIGGER {table_name}_notify_delete
      AFTER DELETE ON {schema}.{table_name}
        FOR EACH ROW
          EXECUTE PROCEDURE {trigger_name}();
"""
