from app.services.coverage import calculate_coverage


def test_calculate_coverage():
    measurements = [
        {"rssi": -64},
        {"rssi": -72},
        {"rssi": -82},
    ]

    result = calculate_coverage(
        measurements
    )

    assert result["total_zones"] == 3
    assert result["covered_zones"] == 2
    assert result["dead_zones"] == 1
    assert result["coverage_percent"] == 66.7
    assert result["average_rssi"] == -72.7


def test_empty_coverage():
    result = calculate_coverage([])

    assert result["total_zones"] == 0
    assert result["coverage_percent"] == 0.0
