import asyncio
from fastapi import APIRouter
import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.decorators.async_task import run_async
from app.utils.logger import get_logger

log = get_logger(__name__)

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("")
async def health() -> dict[str, str]:
    log.info("Health API Triggered")
    return {"response": "Server Is Running"}

@router.get("/concurrent")
async def test_concurrent():
    sendEmail()
    
@run_async
async def sendEmail(db: AsyncSession = None):
    await asyncio.sleep(3)
    log.info("Sending Email")