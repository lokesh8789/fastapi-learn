import asyncio
from datetime import timedelta, datetime
from fastapi import APIRouter, BackgroundTasks

from app.configs.db_config import DBSessionDep
from app.dependencies import CurrentUserDep
from app.models.user import User
from app.schemas.user import UserCreate, UserSchema
from app.services.user_service import UserServiceDep
from app.utils.logger import get_logger


log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User API"],
)


@router.post("/create")
async def create_user(
    req: UserCreate,
    db: DBSessionDep,
    user_service: UserServiceDep,
) -> UserSchema:
    log.info("Creating a new user")
    return await user_service.save_user(db, req)


@router.get("/get-by-id/{id}")
async def get_user(
    id: int,
    db: DBSessionDep,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
    background_tasks: BackgroundTasks,
) -> UserSchema:
    log.info(f"Fetching user by ID with current user is: {current_user.email}")

    background_tasks.add_task(test_task, id, db)
    asyncio.create_task(test_task(id, db))
    return await user_service.get_user_by_id(db, id)


async def test_task(id: int, db: DBSessionDep):
    log.info(f"Testing In Background For Id: {id}")
    await asyncio.sleep(10)
    user = await db.get(User, id)
    log.info(f"user is: {user}")


@router.get("/get-all")
async def get_all_users(
    db: DBSessionDep,
    user_service: UserServiceDep,
) -> list[UserSchema]:
    log.info("Fetching all users")
    return await user_service.get_all_users(db)


@router.delete("/delete/{id}")
async def delete_user(id: int, db: DBSessionDep, user_service: UserServiceDep) -> None:
    log.info("Delete user endpoint called")
    return await user_service.delete_user(db, id)
