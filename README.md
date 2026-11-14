# SPATIALINK
### Where Space Shapes Signal.

**Architecture × Wireless Measurement × Spatial Visualization**

SPATIALINK explores how architectural layouts, building materials, partitions and human occupancy influence indoor 2.4 GHz Wi-Fi measurements. It connects architectural scenario design with an ESP32 field Scout, a FastAPI measurement service and a React console. **Spatial heatmaps and material/occupancy models are research goals, not implemented features.**

## Project leadership

**박하음 — Architectural Research & Design Direction** · Department of Architecture, Pai Chai University  
Spatial analysis, architectural scenarios, material interpretation, visualization concepts and UI/UX direction.

**이영준 — Systems Engineering & Development** · Department of Computer Engineering, Pai Chai University  
ESP32 firmware, system architecture, FastAPI, data storage, React integration and automated validation.

The original SiteLink contribution record is preserved in [Project Origins](docs/project-origins.md). New design responsibilities describe the rebranding direction; completed contributions must be supported by artifacts.

## Architecture

```text
Architectural space & scenarios (research)
                   |
ESP32 Scout / boardless simulator
  2.4 GHz RSSI · SSID · BSSID · channel
                   | HTTP / JSON
                   v
           FastAPI measurement API
                   |
                SQLite
                   |
           React Field Console
                   |
Floor-plan coordinates & spatial layers (planned)
```

## Capabilities and evidence

| Capability | State |
|---|---|
| ESP32 2.4 GHz scanning firmware | Implemented prototype; physical validation pending |
| Measurement / device / coverage API and SQLite | Implemented prototype |
| React field console | Implemented prototype |
| Boardless simulated E2E workflow | Available; synthetic data |
| Sampled-zone RSSI classification | Implemented; not a spatial heatmap |
| Floor-plan coordinate mapping and interactive heatmap | Planned |
| Material and occupancy attenuation modeling | Research; unvalidated |
| CAD/BIM integration | Future |

**Measurement boundary:** the existing coverage percentage counts the latest observed RSSI for each sampled zone (usable at RSSI ≥ -75 dBm). It does not measure continuous floor-plan coverage. RSSI alone cannot isolate material or human attenuation.

## Quick start

Requires a Unix-like shell, Python backend virtual environment at `backend/.venv`, installed frontend dependencies and available ports 8000/5173. See [System Architecture](docs/architecture.md) for setup notes.

```bash
./scripts/start-demo.sh
./scripts/simulate-demo.sh
./scripts/check-demo.sh
./scripts/stop-demo.sh
```

- Frontend: http://localhost:5173
- API schema: http://127.0.0.1:8000/docs
- Simulator sends synthetic telemetry, **not field measurements**.

ESP32 firmware setup, build, upload and monitoring are described in [System Architecture](docs/architecture.md).

## Documentation

| Document | Contents |
|---|---|
| [Spatial Analysis](docs/spatial-analysis.md) | Architectural variables, material/occupancy scenarios and modeling assumptions |
| [System Architecture](docs/architecture.md) | Firmware, backend, frontend, API and execution |
| [Validation Plan](docs/validation-plan.md) | Software versus physical validation, measurement protocol and metrics |
| [Design Direction](docs/design-direction.md) | Architecture-led UX, 4-screen handoff, pending design review |
| [Roadmap](docs/roadmap.md) | Staged development and evidence gates |
| [Project Origins](docs/project-origins.md) | LH competition, simulation figures, original team roles and historical scope |

## Architectural workspace concept (unapproved)

![SPATIALINK conceptual architectural workspace](docs/spatialink-workspace-concept.svg)

**Concept only.** The floor plan, room dimensions, point locations and RSSI labels in this image are synthetic UI placeholders. This is an AI-prepared draft for 박하음's review, **not** an authored or approved deliverable by 박하음 and **not** a currently implemented spatial UI. See [the design handoff](docs/design-direction.md).

## Principles

1. Separate physical measurements, synthetic samples and model estimates.
2. Make spatial coordinates, conditions and data provenance explicit.
3. Treat RSSI as signal-strength evidence, not a complete network-quality metric.
4. Distinguish prototype implementation from planned research.
5. Preserve historical competition claims with their original simulation boundary.

**SPATIALINK — Where Space Shapes Signal.**
