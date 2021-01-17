import time

from app.api.schemas.common import OKResponse
from app.core.utils.timeit import async_timeit
from fastapi import APIRouter

router = APIRouter()


def init_app(app_instance):
    app_instance.include_router(router, tags=["health"])


@router.get("/health", response_model=OKResponse)
@async_timeit
async def health() -> dict:
    return {"status": "ok", "timestamp": int(time.time())}
