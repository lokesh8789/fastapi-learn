from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel

from app.schemas.shipment import ShipmentStatus


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    status: ShipmentStatus = Field(
        sa_column=Column(
            String,
            nullable=False,
        ),
    )
