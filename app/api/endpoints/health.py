import time

from fastapi import APIRouter

from app.api.schemas.common import OKResponse

router = APIRouter()


@router.get("/health", response_model=OKResponse)
async def health() -> dict:
    return {"status": "ok", "timestamp": int(time.time())}
