import logging
from importlib.metadata import entry_points
from typing import Callable
from typing import Optional

from app.core import config
from app.postgres.db.session import db
from fastapi import FastAPI
from poetry.core.masonry.utils import module
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME,
        debug=config.DEBUG,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    load_modules(application)
    db.init_app(application)

    return application


def load_modules(application_instance: Optional[FastAPI] = None):
    for ep in entry_points()["app.modules"]:
        print(f"Loading module: {ep.name}")
        app_module: module = ep.load()
        if application_instance:
            init_app: Callable = getattr(app_module, "init_app", None)
            if init_app:
                init_app(application_instance)
