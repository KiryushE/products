from fastapi import APIRouter, Depends
from .users import fastapi_users, current_active_user, auth_backend
from schemas.users import UserCreate, UserShoppingCart, UserUpdate
from db.models import User


auth_router = APIRouter()


auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)
auth_router.include_router(
    fastapi_users.get_register_router(UserShoppingCart, UserCreate),
    prefix='/auth',
    tags=['auth']
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth']
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserShoppingCart),
    prefix='/auth',
    tags=['auth']
)
auth_router.include_router(
    fastapi_users.get_users_router(UserShoppingCart, UserUpdate),
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/authenticated-only')
async def authenticated_only(curent_user: User = Depends(current_active_user)):
    return {'message': f'Hello, {curent_user.email}'}