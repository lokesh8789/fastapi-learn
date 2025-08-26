from fastapi import APIRouter


router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("")
async def health() -> dict[str, str]:
    print("Health API Triggered")
    return {"response": "Server Is Running"}
