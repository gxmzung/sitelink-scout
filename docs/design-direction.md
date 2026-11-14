# SPATIALINK — Architecture-led UX Design Handoff

> **Status: AI-prepared concept for 박하음 review, not approved or authored by 박하음.**  
> 박하음의 예정 역할: 건축 공간 해석·실험 시나리오·UI/UX 디렉팅. 이영준의 예정 역할: 데이터 모델·백엔드·프론트엔드 구현.  
> **Evidence rule:** 이 문서/시안은 완성된 건축 현장조사나 실제 사용자 테스트의 증거가 아니다.

## Working concept

![SPATIALINK experimental architectural workspace concept](spatialink-workspace-concept.svg)

[Open editable SVG concept](spatialink-workspace-concept.svg)

**Where Space Shapes Signal.** Building geometry is the workspace, not a background decoration. A discrete RSSI observation is a marker with provenance, never a filled heatmap by default.

### Design goals

1. Locate each sample in **metres on a versioned, scaled floor plan**.
2. Distinguish **MEASURED / SYNTHETIC / ESTIMATED / MISSING** in every relevant visual and export.
3. Allow comparison of one changing spatial variable with the **same AP, device position and measurement protocol**.
4. Show a user *why* a value is associated with an architectural feature without claiming causality.
5. Keep clear separation between existing Scout zone telemetry and future coordinate-linked datasets.

## Information architecture

```text
Project
 └── Floor (revision, dimensions, drawing source, x/y origin)
      ├── Scenarios (S01 baseline; S02 partition; S03 wall; S04 occupancy)
      ├── Layers (geometry, wall types, observed samples, estimated layer OFF)
      ├── Point inspector (position, provenance, RSSI, BSSID, time, sample count)
      └── Comparison (baseline vs alternate, uncertainty and notes)
```

### Screen A — Spatial Workspace (concept image above)

- **Left sidebar:** select floor and phase/scenario; toggles for wall/material geometry and samples; estimated field disabled until calibrated.
- **Canvas:** SVG floor plan with north arrow, metre scale bar, origin, revision, door/opening geometry, AP position and individual measurements.
- **Right inspector:** point coordinates, measured/estimated/synthetic tag, raw source, timestamps and device identifiers. Missing values display “Not recorded”, never zero.
- **Bottom:** paired scenario comparison and evidence completeness warnings.

**Prototype interaction:** clicking a point updates the inspector; selecting a scenario changes the annotation set; disabled heatmap has a tooltip explaining required georeferenced evidence. These are **design specifications, not implemented behaviors**.

### Screen B — Scenario Compare (wireframe specification)

```text
┌──────────────────────┬───────────────────────┐
│ S01 OPEN BASELINE    │ S02 PARTITION CHANGE  │
│ plan + observed dots │ same plan + dots      │
│ fixed AP & receiver  │ added wall annotation │
├──────────────────────┴───────────────────────┤
│ P01: baseline median  | alternate median     │
│ ΔRSSI (dB), sample counts, dates, IQR        │
│ [Confounders] [Protocol] [Export CSV]        │
└──────────────────────────────────────────────┘
```

Never compare two conditions as a causal material effect if the AP/channel/device position changed. With no physical readings, all numerical labels must say “SYNTHETIC EXAMPLE”.

### Screen C — Measurement Session (wireframe specification)

```text
Floor / Drawing version / BSSID / Channel / AP height
Point ID / x,y,z (m) / scenario / material / people count
Source: [Physical ESP32] [Synthetic simulator] [Manual import]
Session start -> quality checks -> save raw samples -> summary
```

Incomplete coordinates and missing plan scale block *spatial analysis*, but not the existing zone-based backend ingestion. Do not present the future editor as currently available.

### Screen D — Data Provenance & Export

Export one record per observation with a transparent provenance key and draw revision. A model prediction adds `model_id`, `version`, `method` and uncertainty fields; interpolation must not overwrite physical observations.

## Design system and implementation contract

| Design token | Concept usage | Developer acceptance |
|---|---|---|
| Deep navy `#0c1422` | chrome/background | tokenized CSS, not hard-coded per component |
| Surface `#172638` | panels | AA contrast testing prior to release |
| Mint `#70e0c4` | selected measurement marker | always paired with label/icon |
| Amber `#f2ca83` | caution/synthetic sample | explicit text “SYNTHETIC” |
| Coral `#f28f8f` | weak sample / warning | not an error severity on its own |
| 8 px grid | spacing | retain responsive equivalents |
| Data legend | measured / estimated / synthetic | visible by keyboard and screen reader |

**Do not rely on color alone.** An observed marker must have a point ID, dBm label or accessible description. Estimated regions use a different fill pattern and a method/uncertainty caption. Empty states distinguish “not sampled” from “no signal”.

Responsive: ≥1200 px three-column spatial workspace; 768–1199 px inspector collapsible; below 768 px layer/inspector drawers and pan/zoom canvas. Prefer SVG scalable geometry for prototype; future CAD/BIM import is explicitly out of scope.

## Architectural pilot: conceptual floor, not an actual surveyed plan

- **Synthetic dimensions:** 12 m × 8 m, southwest coordinate origin (0,0), north up; 40 SVG px/m in the drawing.
- **Illustrative positions:** P1 (~2.05,4.95 m), P2 (~4.48,1.45 m), P3 (~9.90,5.55 m).
- **Synthetic labels only:** −62, −74, −82 dBm. **These are UI placeholders and not experiments, claims of RF strength, or material coefficients.**
- **Building geometry:** schematic rooms/doors, not building code-compliant drawings.
- **Follow-up:** replace with permissioned floor plan, measured dimensions, revision identifier and field photos only after review.

### Spatial pilot acceptance (architectural review gate)

| Check | Current status | Evidence required |
|---|---|---|
| Research question and variables defined | Drafted | `docs/spatial-analysis.md` |
| Conceptual UI composition | Drafted; unapproved | `docs/spatialink-workspace-concept.svg` |
| Real building/floor selected | Not started | permitted room/floor identifier |
| Scale and north orientation surveyed | Not started | measured floor-plan metadata |
| Material taxonomy verified in situ | Not started | annotated material schedule |
| Controlled measurement point locations | Not started | accessible, safe, repeated point layout |
| 박하음's design sign-off | Pending | dated feedback or reviewed revision |

## Reviewer handoff for 박하음

Please review **before attributing completed design work**:

1. Whether room/wall/door symbols and annotation hierarchy make sense for architectural practice.
2. Whether the spatial scenarios correspond to realistically controllable building conditions.
3. Whether scale/coordinates and material taxonomy adequately support an on-site measurement plan.
4. Whether the UI helps distinguish observation from prediction at a glance.
5. Which real building can be surveyed safely and with permission.

Record feedback in a PR comment or signed-off revision. **No one has approved this concept on 박하음's behalf.**

## Portfolio evidence

Retain the research question, architectural scenarios, a versioned floor plan, wireframes, design decisions and actual feedback. Use dated authorship records. Treat this AI-prepared exploratory concept as supporting material, not evidence of a third party's personal design contribution.
