#!/usr/bin/env python3

import argparse
import json
import random
import time
import urllib.error
import urllib.request

DEFAULT_API = "http://127.0.0.1:8000/api/v1/measurements"


def post_measurement(api_url, payload):
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            text = response.read().decode("utf-8")
            print(
                f"[SIM] {payload['device_id']} "
                f"{payload['zone_id']} "
                f"{payload['rssi']} dBm "
                f"HTTP {response.status}"
            )
            return text
    except urllib.error.URLError as exc:
        print(f"[SIM] POST failed: {exc}")
        return None


def fixed_scenario():
    return [
        {
            "device_id": "SCOUT-01",
            "zone_id": "ZONE-B03",
            "ssid": "SiteLink_AP_01",
            "bssid": "AA:BB:CC:DD:EE:01",
            "rssi": -64,
            "channel": 6,
        },
        {
            "device_id": "SCOUT-02",
            "zone_id": "ZONE-C02",
            "ssid": "SiteLink_AP_01",
            "bssid": "AA:BB:CC:DD:EE:02",
            "rssi": -82,
            "channel": 6,
        },
        {
            "device_id": "SCOUT-03",
            "zone_id": "ZONE-D01",
            "ssid": "SiteLink_AP_01",
            "bssid": "AA:BB:CC:DD:EE:03",
            "rssi": -89,
            "channel": 6,
        },
    ]


def dynamic_scenario(step):
    base = [
        ("SCOUT-01", "ZONE-B03", -61),
        ("SCOUT-02", "ZONE-C02", -74),
        ("SCOUT-03", "ZONE-D01", -80),
    ]

    result = []

    for index, (device_id, zone_id, rssi) in enumerate(base):
        drift = random.randint(-3, 3)

        # Simulate obstruction appearing around SCOUT-02.
        if device_id == "SCOUT-02" and step >= 5:
            drift -= 10

        result.append(
            {
                "device_id": device_id,
                "zone_id": zone_id,
                "ssid": "SiteLink_AP_01",
                "bssid": f"AA:BB:CC:DD:EE:{index + 1:02d}",
                "rssi": rssi + drift,
                "channel": 6,
            }
        )

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        default=DEFAULT_API,
    )
    parser.add_argument(
        "--mode",
        choices=["fixed", "dynamic"],
        default="dynamic",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=10,
    )

    args = parser.parse_args()

    print("========================================")
    print(" SiteLink Scout Software Simulator")
    print("========================================")
    print(f"API: {args.api}")
    print(f"Mode: {args.mode}")
    print()

    if args.mode == "fixed":
        for measurement in fixed_scenario():
            post_measurement(args.api, measurement)
        return

    for step in range(args.cycles):
        print(f"\n[SIM] cycle {step + 1}/{args.cycles}")

        for measurement in dynamic_scenario(step):
            post_measurement(args.api, measurement)

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
