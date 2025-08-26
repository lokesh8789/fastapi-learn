from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy import text

from app.configs.db_config import async_session
from app.decorator_learn import log
from app.routers import health, shipment


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("App startup")
    async with async_session() as session:
        await session.execute(text("Select 1"))
    yield
    print("App shutdown")


app = FastAPI(
    lifespan=lifespan_handler,
)


@app.get("/scalar", include_in_schema=False)
@log(val="Accessing Scalar Docs")
async def scalar_docs() -> HTMLResponse:
    print("Scalar API reference")
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


## Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


# @app.middleware("http")
# async def custom_middleware(request: Request, call_next):
#     print("Inside custom_middleware")
#     response: Response = await call_next(request)
#     print(f"Returning Response {str(response.body)}")
#     return response


## Routers
app.include_router(health.router)
app.include_router(shipment.router)
