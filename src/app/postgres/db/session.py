import asyncio
from typing import List
from typing import Optional

import asyncpg
from asyncpg.pool import Pool
from gino.declarative import ModelType
from gino_starlette import Gino

from app.core.config import db_settings
from app.postgres.triggers.users_triggers import add_table_triggers
from app.postgres.triggers.users_triggers import create_notify_trigger

db: Gino = Gino(
    dsn=db_settings.DATABASE_URL,
    pool_min_size=db_settings.DB_POOL_MIN_SIZE,
    pool_max_size=db_settings.DB_POOL_MAX_SIZE,
    echo=db_settings.DB_ECHO,
    ssl=db_settings.DB_SSL,
    use_connection_for_request=db_settings.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=db_settings.DB_RETRY_LIMIT,
    retry_interval=db_settings.DB_RETRY_INTERVAL,
)


class DbEventsListener:
    pool: Optional[Pool] = None

    def __init__(self, init_gino: bool = False):
        self.listeners = []

    async def add_listener(self, table_model: ModelType):
        conn: asyncpg.Connection = await self.pool.acquire()
        channel_name: str = await self.__create_table_triggers(conn, table_model)
        await conn.add_listener(channel_name, table_model.db_event)
        self.listeners.append(conn)

    async def connect(self) -> Pool:
        self.pool = await asyncpg.create_pool(db_settings.DATABASE_URL)
        return self.pool

    async def disconnect(self):
        if self.pool:
            releases: List = [self.pool.release(conn) for conn in self.listeners]
            await asyncio.gather(*releases)
            await self.pool.close()

    @staticmethod
    async def __create_table_triggers(db_connection: asyncpg.Connection, table_model: ModelType) -> str:
        table_name: str = table_model.__tablename__
        notification_channel_name: str = f"{table_name}_channel"
        trigger_name: str = f"{table_name}_update_notify_trigger"

        await create_notify_trigger(db_connection, trigger_name, notification_channel_name)
        await add_table_triggers(db_connection, table_name, trigger_name)

        return notification_channel_name

    async def __aenter__(self) -> Pool:
        return await self.connect()

    async def __aexit__(self, *exc):
        await self.disconnect()
