from app.services.signal import SignalStatus, classify_rssi, is_usable


def calculate_coverage(
    zone_measurements: list[dict],
) -> dict:
    total_zones = len(zone_measurements)

    if total_zones == 0:
        return {
            "total_zones": 0,
            "covered_zones": 0,
            "uncovered_zones": 0,
            "dead_zones": 0,
            "coverage_percent": 0.0,
            "average_rssi": None,
        }

    covered_zones = sum(
        1
        for measurement in zone_measurements
        if is_usable(measurement["rssi"])
    )

    uncovered_zones = total_zones - covered_zones

    dead_zones = sum(
        1
        for measurement in zone_measurements
        if classify_rssi(measurement["rssi"]) == SignalStatus.DEAD
    )

    average_rssi = sum(
        measurement["rssi"]
        for measurement in zone_measurements
    ) / total_zones

    return {
        "total_zones": total_zones,
        "covered_zones": covered_zones,
        "uncovered_zones": uncovered_zones,
        "dead_zones": dead_zones,
        "coverage_percent": round(
            covered_zones / total_zones * 100,
            1,
        ),
        "average_rssi": round(
            average_rssi,
            1,
        ),
    }
