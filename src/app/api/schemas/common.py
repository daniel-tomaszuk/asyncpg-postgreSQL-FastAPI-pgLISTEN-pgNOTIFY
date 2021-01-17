from pydantic import BaseModel


class OKResponse(BaseModel):
    status: str
    timestamp: int
