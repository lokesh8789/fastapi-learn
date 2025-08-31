from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.configs.db_config import async_session
from app.exceptions.exception import AuthenticationException
from app.exceptions.problem_details import ProblemDetails
from app.repos.user_repo import get_user_repository
from app.utils.jwt_util import JwtUtil
from app.utils.logger import get_logger

log = get_logger(__name__)

public_paths = [
    "/api/v1/auth/login",
    "/api/v1/users/create",
    "/docs",
    "/openapi.json",
]


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log.info(f"JWTMiddleware: Processing request {request.url.path}")
        try:
            # Skip public endpoints
            if any(request.url.path.startswith(path) for path in public_paths):
                return await call_next(request)

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise AuthenticationException("Missing or invalid Authorization header")

            token = auth_header.split(" ")[1]
            username = JwtUtil.get_username_from_token(token)
            if not username or not JwtUtil.validate_token(token, username):
                raise AuthenticationException("Invalid or expired token")

            user_repo = get_user_repository()
            async with async_session() as db:
                user = await user_repo.find_by_email(db, username)
                if not user:
                    raise AuthenticationException("Username Not Found")
                if user.is_active is False:
                    raise AuthenticationException("User is Inactive")

            request.state.user = user

            return await call_next(request)
        except AuthenticationException as ex:
            return ProblemDetails(
                status=ex.status_code,
                title="Unauthorized",
                detail=ex.message,
            ).to_response()
