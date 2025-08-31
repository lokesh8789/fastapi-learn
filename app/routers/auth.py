from fastapi import APIRouter

from app.configs.db_config import DBSessionDep
from app.schemas.auth import AuthReponse, LoginRequest
from app.services.auth_service import AuthServiceDep
from app.utils.logger import get_logger

log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(
    request: LoginRequest,
    db: DBSessionDep,
    auth_service: AuthServiceDep,
) -> AuthReponse:
    log.info(f"Login request received for email: {request.email}")
    return await auth_service.login(request, db)
