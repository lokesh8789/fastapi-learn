import asyncio
from datetime import timedelta, datetime
import time
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Header
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlmodel import select

from app.configs.db_config import DBSessionDep
from app.dependencies import CurrentUserDep
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserSchema
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


@router.get("get-by-email")
async def get_by_email(
    email: str,
    db: DBSessionDep,
    authorization: Annotated[str | None, Header()] = None,
) -> list[UserResponse]:
    log.info("Finding By Email")
    if authorization:
        log.info(f"Authorization : {authorization}")
    # result = await db.execute(select(User.id, User.name).where(User.email == email))
    result = await db.execute(
        text("select id, name from users where email = :email"),
        {
            "email": email,
        },
    )
    # users = result.all()  # List of tuples: [(id1, username1), (id2, username2), ...]
    # return [{"id": u[0]} for u in users]
    return [UserResponse(**data) for data in result.mappings().all()]


@router.get("/sse")
async def sse():
    log.info("Streaming Response Testing")
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


async def event_generator():
    """Yield messages indefinitely every 1 second"""
    counter = 0
    while True:
        counter += 1
        yield f"data: Message {counter} at {time.strftime('%X')}\n\n"
        await asyncio.sleep(1)
