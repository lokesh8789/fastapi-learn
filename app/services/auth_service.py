from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from app.configs.db_config import DBSessionDep
from app.exceptions.exception import AuthenticationException
from app.repos.user_repo import UserRepository, UserRepositoryDep
from app.schemas.auth import AuthReponse, LoginRequest
from app.schemas.user import UserSchema
from app.utils.bcrypt_util import verify_text
from app.utils.jwt_util import JwtUtil


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def login(self, request: LoginRequest, db: DBSessionDep) -> AuthReponse:
        user = await self.user_repo.find_by_email(db, request.email)
        if not user:
            raise AuthenticationException("Invalid Email Id")
        if user.is_active is False:
            raise AuthenticationException("User is Inactive")
        if not verify_text(request.password, user.password):
            raise AuthenticationException("Invalid Password")

        token = JwtUtil.generate_token(user.email)

        return AuthReponse(
            user=UserSchema(
                **user.model_dump(),
            ),
            token=token,
        )


@lru_cache
def get_auth_service(user_repo: UserRepositoryDep) -> AuthService:
    return AuthService(user_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
