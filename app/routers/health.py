from fastapi import APIRouter

from app.utils.logger import get_logger

log = get_logger(__name__)

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("")
async def health() -> dict[str, str]:
    log.info("Health API Triggered")
    return {"response": "Server Is Running"}
