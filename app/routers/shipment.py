from fastapi import APIRouter, status

from app.configs.db_config import DBSessionDep
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from app.services.shipment_service import ShipmentServiceDep

router = APIRouter(prefix="/api/v1/shipments", tags=["Shipment API"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_shipment(
    req: ShipmentCreate,
    db: DBSessionDep,
    shipment_service: ShipmentServiceDep,
) -> ShipmentResponse:
    return await shipment_service.create_shipment(db, req)


@router.put("/update/{id}")
async def update_shipment(
    id: int,
    req: ShipmentUpdate,
    db: DBSessionDep,
    shipment_service: ShipmentServiceDep,
) -> ShipmentResponse:
    return await shipment_service.update_shipment(db, id, req)


@router.delete("/delete/{id}")
async def delete_shipment(
    id: int,
    db: DBSessionDep,
    shipment_service: ShipmentServiceDep,
) -> None:
    await shipment_service.delete_shipment(db, id)
    return None


@router.get("/get-by-id/{id}", status_code=status.HTTP_200_OK)
async def get_shipment(
    id: int,
    db: DBSessionDep,
    shipment_service: ShipmentServiceDep,
) -> ShipmentResponse:
    return await shipment_service.get_shipment_by_id(db, id)


@router.get("/get-all", status_code=status.HTTP_200_OK)
async def list_shipments(
    db: DBSessionDep,
    shipment_service: ShipmentServiceDep,
) -> list[ShipmentResponse]:
    return await shipment_service.get_all_shipments(db)
