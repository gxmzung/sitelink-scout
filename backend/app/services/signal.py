from enum import Enum


class SignalStatus(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    DEAD = "DEAD"


def classify_rssi(rssi: int) -> SignalStatus:
    if rssi >= -55:
        return SignalStatus.EXCELLENT

    if rssi >= -65:
        return SignalStatus.GOOD

    if rssi >= -75:
        return SignalStatus.FAIR

    if rssi >= -85:
        return SignalStatus.POOR

    return SignalStatus.DEAD


def is_usable(rssi: int) -> bool:
    return rssi >= -75
