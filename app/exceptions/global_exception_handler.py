from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.exception import (
    BusinessException,
    AlreadyExistsException,
    NotFoundException,
)
from app.exceptions.problem_details import ProblemDetails
from app.utils.logger import get_logger

log = get_logger(__name__)


def global_exception_handler(app: FastAPI) -> None:

    @app.exception_handler(NotFoundException)
    def handle_user_not_found_exception(
        request: Request,
        ex: NotFoundException,
    ) -> JSONResponse:
        log.info("Handling UserNotFoundException")
        return ProblemDetails(
            status=ex.status_code,
            title="Not Found",
            detail=ex.message,
        ).to_response()

    @app.exception_handler(AlreadyExistsException)
    def handle_user_already_exists_exception(
        request: Request,
        ex: AlreadyExistsException,
    ) -> JSONResponse:
        log.info("Handling UserAlreadyExistsException")
        return ProblemDetails(
            status=ex.status_code,
            title="Already Exists",
            detail=ex.message,
        ).to_response()

    @app.exception_handler(BusinessException)
    def handle_business_exception(
        request: Request,
        ex: BusinessException,
    ) -> JSONResponse:
        log.info("Handling BusinessException")
        return ProblemDetails(
            status=ex.status_code,
            title="Bad Request",
            detail=ex.message,
        ).to_response()

    @app.exception_handler(HTTPException)
    def handle_http_exception(
        request: Request,
        ex: HTTPException,
    ) -> JSONResponse:
        log.info("Handling HTTPException")
        return ProblemDetails(
            status=ex.status_code,
            title="Bad Request",
            detail=ex.detail,
        ).to_response()

    @app.exception_handler(Exception)
    def handle_exception(
        request: Request,
        ex: Exception,
    ) -> JSONResponse:
        log.error(f"Handling generic Exception: {str(ex)}")
        return ProblemDetails(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Internal Server Error",
            detail=str(ex),
        ).to_response()
