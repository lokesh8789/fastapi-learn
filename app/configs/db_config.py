from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.configs.app_config import settings

engine: AsyncEngine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)

async_session: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
