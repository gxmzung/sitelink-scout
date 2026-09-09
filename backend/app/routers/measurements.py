from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.measurement import Measurement
from app.schemas.measurement import (
    MeasurementCreate,
    MeasurementResponse,
)

router = APIRouter(
    prefix="/api/v1/measurements",
    tags=["measurements"],
)


@router.post(
    "",
    response_model=MeasurementResponse,
    status_code=201,
)
def create_measurement(
    payload: MeasurementCreate,
    db: Session = Depends(get_db),
):
    measurement = Measurement(
        **payload.model_dump()
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    return measurement


@router.get(
    "",
    response_model=List[MeasurementResponse],
)
def list_measurements(
    limit: int = 100,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 500))

    statement = (
        select(Measurement)
        .order_by(desc(Measurement.received_at))
        .limit(limit)
    )

    return list(
        db.scalars(statement).all()
    )
