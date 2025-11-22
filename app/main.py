from contextlib import asynccontextmanager
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from sqlalchemy import text

from app.configs.db_config import async_session
from app.exceptions.global_exception_handler import global_exception_handler
from app.middlewares.jwt_middleware import JWTMiddleware
from app.models.user import User
from app.routers import auth, health, shipment, user
from app.utils.logger import get_logger
from app.configs.schedule_config import scheduler, scheduled
from app.configs.db_config import AsyncSession

log = get_logger(__name__)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    log.info("App startup")
    async with async_session() as session:
        await session.execute(text("Select 1"))
    scheduler.start()
    yield
    scheduler.shutdown()
    log.info("App shutdown")


app = FastAPI(
    lifespan=lifespan_handler,
    docs_url=None,
    redoc_url=None,
)


@scheduled(cron="25 33 3 * * *", zone="Asia/Kolkata")
async def test_scheduler(db: AsyncSession):
    log.info("Hi Schduler is running")
    user = await db.get(User, 1)
    log.info(f"User is: {user}")


# @scheduled(fixedRate=1000)
# def test_scheduler2():
#     log.info("Hi Schduler2 is running")
#     time.sleep(2)
#     log.info("Sleep Completed")


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    log.info("Scalar API reference")
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


## Exception Handler
global_exception_handler(app)

## Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

app.add_middleware(JWTMiddleware)


# def middle(request: Request, call_next):
#     log.info(f"Inside custom middleware for {request.url.path}")
#     response = call_next(request)
#     log.info(f"Returning Response {str(response.body)}")
#     return response


# app.middleware("http")(middle)


# @app.middleware("http")
# async def custom_middleware(request: Request, call_next):
#     log.info("Inside custom_middleware")
#     response: Response = await call_next(request)
#     log.info(f"Returning Response {str(response.body)}")
#     return response


## Routers
app.include_router(health.router)
app.include_router(shipment.router)
app.include_router(user.router)
app.include_router(auth.router)
