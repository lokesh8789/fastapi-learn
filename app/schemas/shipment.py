from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    delivered = "delivered"
    pending = "pending"
    out_for_delivery = "out_for_delivery"


class ShipmentCreate(BaseModel):
    id: int | None = Field(
        default=None,
    )
    status: ShipmentStatus

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus

class ShipmentResponse(BaseModel):
    id: int
    status: ShipmentStatus