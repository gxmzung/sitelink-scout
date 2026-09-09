from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    device_id: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    zone_id: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    ssid: Mapped[str] = mapped_column(
        String(128),
    )

    bssid: Mapped[str] = mapped_column(
        String(32),
    )

    rssi: Mapped[int] = mapped_column(
        Integer,
    )

    channel: Mapped[int] = mapped_column(
        Integer,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
