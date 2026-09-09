from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.measurement import Measurement
from app.services.signal import classify_rssi

router = APIRouter(
    prefix="/api/v1/devices",
    tags=["devices"],
)


def serialize_measurement(measurement: Measurement):
    return {
        "device_id": measurement.device_id,
        "zone_id": measurement.zone_id,
        "ssid": measurement.ssid,
        "bssid": measurement.bssid,
        "rssi": measurement.rssi,
        "channel": measurement.channel,
        "signal_status": classify_rssi(measurement.rssi).value,
        "received_at": measurement.received_at,
    }


@router.get("")
def list_devices(
    db: Session = Depends(get_db),
):
    device_ids = db.scalars(
        select(Measurement.device_id).distinct()
    ).all()

    devices = []

    for device_id in device_ids:
        latest = db.scalar(
            select(Measurement)
            .where(Measurement.device_id == device_id)
            .order_by(Measurement.received_at.desc())
            .limit(1)
        )

        if latest is not None:
            devices.append(
                serialize_measurement(latest)
            )

    return devices


@router.get("/{device_id}")
def get_device(
    device_id: str,
    db: Session = Depends(get_db),
):
    latest = db.scalar(
        select(Measurement)
        .where(Measurement.device_id == device_id)
        .order_by(Measurement.received_at.desc())
        .limit(1)
    )

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return serialize_measurement(latest)
