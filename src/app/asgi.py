import uvicorn
from fastapi import FastAPI
from postgres.db.session import DbEventsListener

from app.main import get_application
from app.postgres.models.users import User

asgi_app: FastAPI = get_application()
db_events_listener: DbEventsListener = DbEventsListener()


@asgi_app.on_event("startup")
async def add_app_db_events_listeners():
    await db_events_listener.connect()
    await db_events_listener.add_listener(User)


@asgi_app.on_event("shutdown")
async def add_app_db_events_listeners():
    await db_events_listener.disconnect()


if __name__ == "__main__":
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)
