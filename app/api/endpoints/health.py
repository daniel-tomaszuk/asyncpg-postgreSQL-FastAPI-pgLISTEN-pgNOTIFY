import time

from fastapi import APIRouter

from app.api.schemas.common import OKResponse
from app.core.utils.timeit import async_timeit

router = APIRouter()


@router.get("/health", response_model=OKResponse)
@async_timeit
async def health() -> dict:
    return {"status": "ok", "timestamp": int(time.time())}
