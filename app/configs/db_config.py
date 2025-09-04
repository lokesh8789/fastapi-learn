from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.configs.app_config import settings

engine: AsyncEngine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=False,
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
