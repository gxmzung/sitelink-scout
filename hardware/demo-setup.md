# SiteLink Scout Demo Setup

## Objective

Demonstrate that SiteLink Scout can measure the actual Wi-Fi environment and send field measurements to the SiteLink Field Console.

## Demo Flow

```text
Wi-Fi AP
   ↓
ESP32 Scout
   ↓
RSSI / BSSID / Channel
   ↓ HTTP JSON
FastAPI
   ↓
SQLite
   ↓
React Field Console
Demo Nodes
SCOUT-01
Zone: ZONE-B03
Role: reference / strong-signal position
SCOUT-02
Zone: ZONE-C02
Role: obstruction / weak-signal position
Physical Demo Concept
Place AP and Scout at fixed locations.
Record baseline RSSI.
Insert foam-board or wall mock-up between AP and Scout.
Observe RSSI degradation.
Remove or reposition the obstruction.
Confirm RSSI recovery.
Display changes in the Field Console.
MVP Metrics

Primary:

RSSI
BSSID
Wi-Fi channel
latest measured sample usability

Prototype usable threshold:

RSSI >= -75 dBm

Signal labels:

= -55: EXCELLENT

-56 to -65: GOOD
-66 to -75: FAIR
-76 to -85: POOR
<= -86: DEAD

These thresholds are prototype indicators, not universal construction-site RF requirements.

Future Metrics
latency
packet loss
jitter
throughput
channel utilization
Hardware Validation Pending

Physical ESP32 upload and real RF measurement collection remain pending.
