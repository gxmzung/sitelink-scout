from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MeasurementCreate(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)
    zone_id: str = Field(min_length=1, max_length=64)
    ssid: str = Field(min_length=1, max_length=128)
    bssid: str = Field(min_length=1, max_length=32)
    rssi: int = Field(ge=-127, le=0)
    channel: int = Field(ge=1, le=14)


class MeasurementResponse(MeasurementCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    received_at: datetime
