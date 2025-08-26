from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db_config import get_db_session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

from app.repos.shipment_repo import ShipmentRepository, get_shipment_repository

ShipmentRepositoryDep = Annotated[ShipmentRepository, Depends(get_shipment_repository)]

from app.services.shipment_service import ShipmentService, get_shipment_service

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
