from app.api.schemas.users import UserIdSchemaOut
from app.api.schemas.users import UserSchemaIn
from app.api.schemas.users import UserSchemaOut
from app.core.utils.timeit import async_timeit
from app.postgres.models.users import User
from fastapi import APIRouter

GET_USER_ID_URL = "/users/{user_id}"
POST_USER_URL = "/users"
DELETE_USER_ID_URL = "/users/{user_id}"


router = APIRouter()


def init_app(app_instance):
    app_instance.include_router(router, tags=["users"])


@router.get(GET_USER_ID_URL, response_model=UserSchemaOut)
@async_timeit
async def get_user(user_id: int):
    user = await User.get_or_404(user_id)
    return user.to_dict()


@router.post(POST_USER_URL, response_model=UserSchemaOut)
@async_timeit
async def add_user(user: UserSchemaIn):
    created_user: User = await User.create(nickname=user.nickname)
    return created_user.to_dict()


@router.delete(DELETE_USER_ID_URL, response_model=UserIdSchemaOut)
@async_timeit
async def delete_user(user_id: int):
    user = await User.get_or_404(user_id)
    await user.delete()
    return dict(id=user_id)
