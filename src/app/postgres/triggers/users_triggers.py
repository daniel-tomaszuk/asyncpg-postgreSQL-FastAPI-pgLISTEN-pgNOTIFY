import asyncpg

from app.postgres.triggers.templates import SQL_CREATE_TRIGGER
from app.postgres.triggers.templates import SQL_TABLE_DELETE
from app.postgres.triggers.templates import SQL_TABLE_INSERT
from app.postgres.triggers.templates import SQL_TABLE_UPDATE


async def create_notify_trigger(connection: asyncpg.Connection, trigger_name: str, channel: str) -> None:
    await connection.execute("CREATE EXTENSION IF NOT EXISTS hstore")
    await connection.execute(SQL_CREATE_TRIGGER.format(trigger_name=trigger_name, channel=channel))


async def add_table_triggers(
    connection: asyncpg.Connection, table_name: str, trigger_name: str, schema: str = "public"
) -> None:
    templates = (
        SQL_TABLE_INSERT,
        SQL_TABLE_UPDATE,
        SQL_TABLE_DELETE,
    )

    for template in templates:
        await connection.execute(template.format(table_name=table_name, trigger_name=trigger_name, schema=schema))
