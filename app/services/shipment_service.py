from functools import lru_cache

from fastapi import Depends, HTTPException

from app.dependencies import DBSessionDep, ShipmentRepositoryDep
from app.models.shipment import Shipment
from app.repos.shipment_repo import ShipmentRepository
from app.schemas.shipment import ShipmentCreate, ShipmentResponse


class ShipmentService:
    def __init__(
        self,
        shipment_repo: ShipmentRepository,
    ) -> None:
        self.shipment_repo = shipment_repo

    async def create_shipment(
        self, db: DBSessionDep, request: ShipmentCreate
    ) -> ShipmentResponse:
        shipment = await self.shipment_repo.save(
            db,
            Shipment(
                **request.model_dump(exclude_none=True),
            ),
        )
        return ShipmentResponse(
            **shipment.model_dump(),
        )

    async def get_shipment_by_id(
        self, db: DBSessionDep, shipment_id: int
    ) -> ShipmentResponse | None:
        shipment = await self.shipment_repo.find_by_id(
            db,
            shipment_id,
        )

        if shipment:
            return ShipmentResponse(
                **shipment.model_dump(),
            )

        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    async def get_all_shipments(self, db: DBSessionDep) -> list[ShipmentResponse]:
        shipments = await self.shipment_repo.find_all(db)
        return [
            ShipmentResponse(
                **shipment.model_dump(),
            )
            for shipment in shipments
        ]

    async def update_shipment(
        self, db: DBSessionDep, shipment_id: int, request: ShipmentCreate
    ) -> ShipmentResponse:
        shipment = await self.shipment_repo.find_by_id(
            db,
            shipment_id,
        )

        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found",
            )

        for key, value in request.model_dump(exclude_none=True).items():
            setattr(shipment, key, value)

        shipment = await self.shipment_repo.save(db, shipment)

        return ShipmentResponse(
            **shipment.model_dump(),
        )

    async def delete_shipment(self, db: DBSessionDep, shipment_id: int) -> None:
        shipment = await self.shipment_repo.find_by_id(
            db,
            shipment_id,
        )

        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found",
            )

        await self.shipment_repo.delete(db, shipment)
        return None


@lru_cache
def get_shipment_service(
    shipment_repository: ShipmentRepositoryDep,
) -> ShipmentService:
    print("Creating ShipmentService")
    return ShipmentService(
        shipment_repo=shipment_repository,
    )
