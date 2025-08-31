from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from app.configs.db_config import DBSessionDep
from app.models.user import User
from app.repos.user_repo import UserRepository, UserRepositoryDep
from app.schemas.user import UserCreate, UserSchema


class UserService:
    def __init__(self, user_Repo: UserRepository) -> None:
        self.user_repo = user_Repo

    async def save_user(self, db: DBSessionDep, req: UserCreate) -> UserSchema:
        user = await self.user_repo.save(db, User(**req.model_dump(exclude_none=True)))
        return UserSchema(**user.model_dump())

    async def get_user_by_id(self, db: DBSessionDep, user_id: int) -> UserSchema:
        user = await self.user_repo.find_by_id(db, user_id)
        if user:
            return UserSchema(**user.model_dump())
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    async def get_all_users(self, db: DBSessionDep) -> list[UserSchema]:
        return [
            UserSchema(**user.model_dump())
            for user in await self.user_repo.find_all(db)
        ]

    async def delete_user(self, db: DBSessionDep, user_id: int) -> None:
        return await self.user_repo.delete(db, user_id)


@lru_cache
def get_user_service(user_repo: UserRepositoryDep) -> UserService:
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
