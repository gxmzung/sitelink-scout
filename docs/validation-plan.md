# Validation Plan

**Spatial protocol:** 박하음 · **Measurement engineering:** 이영준

## Evidence levels

| Level | Goal | Evidence | Limit |
|---|---|---|---|
| V0 | Boardless E2E | tests, API, logs, UI | synthetic samples |
| V1 | Physical ESP32 | real scan, BSSID/channel, POST | not RF calibration |
| V2 | Spatial comparisons | repeated paired RSSI and drawings | confounders remain |
| V3 | Model accuracy | held-out physical measurements | scenario-limited |

## Controlled pilot

1. Select a scaled floor plan, record AP/receiver x/y and heights.
2. Fix AP model, BSSID, channel, power, antenna orientation and device position.
3. Record baseline geometry, materials, thickness and occupancy.
4. Compare open space, partitions, concrete barriers, material arrangements and occupancy scenarios separately.
5. Initially collect 30 readings per point/condition across multiple independent sessions; **30 is a pilot choice, not a statistically justified sample size**.
6. Save raw observations, timestamps, source type, configuration and floor-plan version.
7. Compare median RSSI, IQR, standard deviation and run-to-run variability.
8. Evaluate any prediction with MAE/RMSE (dB) on held-out physical points against a baseline.

Define numerical accuracy targets after pilot variability is measured; report uncertainty and confounders.

## Acceptance

V0 requires reproducible API and E2E passes. V1 requires physical device-to-console data flow. V2 requires repeatable, documented paired experiments. V3 requires predeclared held-out evaluation. Simulated values cannot establish real-world material attenuation.

## Historical boundary

The LH proposal-stage simulation tested 454 AP candidates, one ~6.3 m relocation and 76.0% → 79.1% priority-zone **predicted** coverage (+3.1 percentage points). These are not physical measurements.

## Evidence archive

Preserve raw CSV/JSON, floor-plan version, setup photos where consented, device settings, software commit, analysis scripts, scenario manifest, figures and limitations. Do not collect personally identifying occupancy records.
