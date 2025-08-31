from functools import lru_cache
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import select
from app.configs.db_config import DBSessionDep
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
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        await db.delete(user)
        await db.commit()


@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
