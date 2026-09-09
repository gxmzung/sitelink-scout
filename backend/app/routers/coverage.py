from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.measurement import Measurement
from app.services.coverage import calculate_coverage
from app.services.signal import classify_rssi

router = APIRouter(
    prefix="/api/v1/coverage",
    tags=["coverage"],
)


@router.get("")
def get_coverage(
    db: Session = Depends(get_db),
):
    zone_ids = db.scalars(
        select(Measurement.zone_id).distinct()
    ).all()

    latest_zones = []

    for zone_id in zone_ids:
        latest = db.scalar(
            select(Measurement)
            .where(Measurement.zone_id == zone_id)
            .order_by(Measurement.received_at.desc())
            .limit(1)
        )

        if latest is None:
            continue

        latest_zones.append(
            {
                "zone_id": latest.zone_id,
                "device_id": latest.device_id,
                "rssi": latest.rssi,
                "signal_status": classify_rssi(
                    latest.rssi
                ).value,
                "received_at": latest.received_at,
            }
        )

    summary = calculate_coverage(
        latest_zones
    )

    return {
        **summary,
        "usable_threshold_dbm": -75,
        "zones": latest_zones,
    }
