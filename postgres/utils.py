import asyncio
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Dict
from typing import List
from typing import Optional

import asyncpg
from asyncpg.pool import Pool

from app.core.config import db_settings


CREATE_DB = "CREATE DATABASE {db_name}"
DROP_DB = "DROP DATABASE {db_name}"


DB_SERVER = "postgresql://{db_user}@{db_host}:{db_port}"
DB_CONNECTION_STRING = DB_SERVER + "/{db_name}"


class PgDatabase:
    def __init__(self, db_name: str, **kwargs):
        self.db_name: str = db_name
        self.params: Dict[str, Any] = dict(
            db_user=db_settings.db_user,
            db_host=db_settings.db_host,
            db_port=db_settings.db_port,
            db_name=db_settings.db_name,
        )
        self.pool: Optional[Pool] = None
        self.owner: bool = kwargs.get("owner", False)
        self.listeners: List = []

    async def connect(self) -> Pool:
        if self.owner:
            await self.server_command(CREATE_DB.format(self.db_name))

        self.pool = await asyncpg.create_pool(DB_CONNECTION_STRING.format(**self.params))
        return self.pool

    async def disconnect(self):
        if self.pool:
            releases: List[Coroutine] = [self.pool.release(connection) for connection in self.listeners]
            await asyncio.gather(releases)
            await self.pool.close()

        if self.owner:
            await self.server_command(DROP_DB.format(**self.params))

    async def server_command(self, command: str):
        connection = await asyncpg.connect(DB_SERVER.format(**self.params))
        await connection.execute(command)
        await connection.close()

    async def add_listener(self, channel_name: str, callback: Callable):
        """
        Create long lived socket connection to the DB.
        Listen to given channel on the DB side.
        """
        connection: asyncpg.Connection = await self.pool.acquire()
        await connection.add_listener(channel_name, callback)
        self.listeners.append(connection)

    async def __aenter__(self) -> Pool:
        return await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
