from typing import Any
from typing import Dict

import asyncpg
import ujson
from boltons.cacheutils import LRU

from app.core.config import settings
from app.postgres.db.session import db

CACHE = LRU(max_size=settings.CACHE_ITEMS_MAX_SIZE)


class User(db.Model):
    __USER_CACHE_KEY = "USERS:ID:{user_id}"
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    nickname = db.Column(db.Unicode(), default="unnamed")

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> "User":
        cache_key: str = cls.__get_cache_key(user_id)
        if cache_key not in CACHE:
            print(f"User {user_id} cache MISS.")
            fetched_user: User = await cls.get_or_404(user_id)
            CACHE[cache_key]: User = fetched_user
        return CACHE[cache_key]

    @classmethod
    def db_event(cls, con_ref: asyncpg.Connection, pid: int, channel: str, payload: str):
        event: Dict[str, Any] = ujson.loads(payload)
        print(f"Got DB event:\n{event}")

        event_id: int = event.get("id")
        event_type: str = event.get("type")
        event_data: Dict[str, Any] = event.get("data", {})
        cache_key: str = cls.__get_cache_key(event_id)

        if event_type == "INSERT":
            CACHE[cache_key]: Dict[str, Any] = event_data
        elif event_type == "UPDATE":
            CACHE[cache_key]: Dict[str, Any] = event_data.get("new", {})
        elif event_type == "DELETE":
            CACHE[cache_key] = None

    @classmethod
    def __get_cache_key(cls, user_id: int) -> str:
        return cls.__USER_CACHE_KEY.format(user_id=user_id)
