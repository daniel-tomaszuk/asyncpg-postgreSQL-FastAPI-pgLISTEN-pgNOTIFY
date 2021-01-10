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


settings = AppSettings()

PROJECT_NAME = settings.PROJECT_NAME
DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS
