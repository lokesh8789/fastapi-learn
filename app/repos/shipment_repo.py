from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from app.configs.db_config import DBSessionDep
from app.models.shipment import Shipment
from app.utils.logger import get_logger

log = get_logger(__name__)

class ShipmentRepository:

    async def save(self, db: DBSessionDep, shipment: Shipment) -> Shipment:
        db.add(shipment)
        await db.commit()
        await db.refresh(shipment)
        return shipment

    async def find_by_id(self, db: DBSessionDep, shipment_id: int) -> Shipment | None:
        return await db.get(Shipment, shipment_id)

    async def find_all(self, db: DBSessionDep) -> list[Shipment]:
        result = await db.execute(select(Shipment))
        return list(result.scalars().all())

    async def delete(self, db: DBSessionDep, shipment: Shipment) -> None:
        await db.delete(shipment)
        await db.commit()


@lru_cache
def get_shipment_repository() -> ShipmentRepository:
    log.info("Creating ShipmentRepository")
    return ShipmentRepository()

ShipmentRepositoryDep = Annotated[ShipmentRepository, Depends(get_shipment_repository)]
