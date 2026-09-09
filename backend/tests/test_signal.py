from app.services.signal import (
    SignalStatus,
    classify_rssi,
    is_usable,
)


def test_signal_boundaries():
    assert classify_rssi(-55) == SignalStatus.EXCELLENT
    assert classify_rssi(-56) == SignalStatus.GOOD
    assert classify_rssi(-65) == SignalStatus.GOOD
    assert classify_rssi(-66) == SignalStatus.FAIR
    assert classify_rssi(-75) == SignalStatus.FAIR
    assert classify_rssi(-76) == SignalStatus.POOR
    assert classify_rssi(-85) == SignalStatus.POOR
    assert classify_rssi(-86) == SignalStatus.DEAD


def test_usable_threshold():
    assert is_usable(-75) is True
    assert is_usable(-76) is False
