from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from app.configs.db_config import DBSessionDep
from app.exceptions.exception import NotFoundException
from app.models.user import User


class UserRepository:
    async def save(self, db: DBSessionDep, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def find_by_id(self, db: DBSessionDep, user_id: int) -> User | None:
        return await db.get(User, user_id)

    async def find_all(self, db: DBSessionDep) -> list[User]:
        result = await db.execute(select(User))
        return list(result.scalars().all())

    async def delete(self, db: DBSessionDep, user_id: int) -> None:
        user = await self.find_by_id(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        await db.delete(user)
        await db.commit()

    async def find_by_email(self, db: DBSessionDep, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().one_or_none()


@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
