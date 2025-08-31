from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ProblemDetails(BaseModel):
    type: str | None = None  # URI identifier for the error
    status: int  # HTTP status code
    title: str  # Short human-readable summary
    detail: str | None = None  # More detailed description
    instance: str | None = None  # URI of the request/resource

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status, content=self.model_dump(exclude_none=True)
        )
