import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import FastAPIUsers, BaseUserManager, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from db.models import User
from db.session import get_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_db(session=Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = "a2de83a0-6af7-4991-aee7-7bf46a82738e"
    verification_token_secret = "a2de83a0-6af7-4991-aee7-7bf46a82738e"

    async def on_after_register(self, user, request: Optional[Request] = None):
        print(f"User {user.email} has registered")

    async def on_after_forgot_password(
        self, user, token, request: Optional[Request] = None
    ):
        print(f"User: {user.email} forgot password. Reset token: {token}")

    async def on_after_request_verify(
        self, user, token, request: Optional[Request] = None
    ):
        print(f"User: {user.email} sended verification request. token: {token}")

    def parse_id(self, user_id):
        return int(user_id)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_stategy() -> JWTStrategy:
    return JWTStrategy(
        secret="a2de83a0-6af7-4991-aee7-7bf46a82738e", lifetime_seconds=3600
    )


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_stategy
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)