from typing import Any
from typing import List

from starlette.datastructures import Secret


class AppSettings:
    SecretKey: Secret
    DEBUG: bool = True
    PROJECT_NAME: str = "Asyncpg-FastAPI"
    ALLOWED_HOSTS: List[str] = ["*"]

    @staticmethod
    def _prepare_debug(val: Any) -> bool:
        return str(val).lower() in ("true", "1")


class DBSettings:
    db_user: str = "postgres"
    db_host: str = "postgres"
    db_name: str = "postgres"
    db_port: int = 5432


settings = AppSettings()
db_settings = DBSettings()

PROJECT_NAME = settings.PROJECT_NAME
DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS
