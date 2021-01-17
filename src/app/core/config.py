import os
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List
from typing import Optional

from starlette.datastructures import Secret


def get_default_allowed_hosts() -> List[str]:
    return os.environ.get("ALLOWED_HOSTS") or ["*"]


@dataclass
class AppSettings:

    SECRET_KEY: Secret = os.environ.get("SECRET_KEY")
    DEBUG: bool = True
    PROJECT_NAME: str = "Asyncpg-FastAPI"
    ALLOWED_HOSTS: List[str] = field(default_factory=get_default_allowed_hosts)

    @staticmethod
    def _prepare_debug(val: Any) -> bool:
        return str(val).lower() in ("true", "1")


@dataclass
class DbConnectorSettings:
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    DB_POOL_MIN_SIZE: int = os.environ.get("DB_POOL_MIN_SIZE", 1)
    DB_POOL_MAX_SIZE: int = os.environ.get("DB_POOL_MAX_SIZE", 16)
    DB_ECHO: bool = os.environ.get("DB_ECHO", False)
    DB_SSL: Optional = os.environ.get("DB_SSL")
    DB_USE_CONNECTION_FOR_REQUEST: bool = os.environ.get("DB_USE_CONNECTION_FOR_REQUEST", True)
    DB_RETRY_LIMIT: int = os.environ.get("DB_RETRY_LIMIT", 1)
    DB_RETRY_INTERVAL: int = os.environ.get("DB_RETRY_INTERVAL", 1)


settings = AppSettings()
db_settings = DbConnectorSettings()

PROJECT_NAME = settings.PROJECT_NAME
DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS
