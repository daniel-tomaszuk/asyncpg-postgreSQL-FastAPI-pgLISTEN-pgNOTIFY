from pydantic import BaseModel


class UserSchemaIn(BaseModel):
    nickname: str


class UserIdSchemaOut(BaseModel):
    id: int


class UserSchemaOut(UserIdSchemaOut):
    nickname: str
