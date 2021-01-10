import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core import config


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, openapi_url="/docs/store-management/openapi.json"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router)
    return application


app = get_application()


if __name__ == "__main__":
    # entrypoint for starting the app as python script - `python main.py` will start the worker
    uvicorn.run(app, host="0.0.0.0", port=8000)
