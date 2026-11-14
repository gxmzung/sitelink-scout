# SPATIALINK Roadmap

Stages are proposed; none implies unverified functionality is complete.

| Stage | Scope | Exit evidence |
|---|---|---|
| 0. Foundation | Documentation, existing E2E and API audit | reproducible checks and preserved history |
| 1. Spatial mapping | floor-plan scale, origin, measurement x/y and provenance | observed points on a correctly scaled plan |
| 2. Architecture-led UX | layers, inspector, scenario comparison | working interface and design rationale |
| 3. Controlled RF study | partitions, concrete, materials, occupancy | raw paired experiments and uncertainty |
| 4. Model evaluation | calibrated coefficients, held-out comparison | baseline, MAE/RMSE and limitations |
| 5. Advanced integrations | CAD/BIM and other wireless technologies | independently scoped validation |

## Ownership

박하음: architectural scenarios, spatial analysis and UX/design direction.  
이영준: firmware, API, data pipeline, frontend implementation and automation.  
Both: experiment design, data interpretation and evidence review.

## Priority

**Spatial coordinates and provenance precede heatmap interpolation.** Avoid arbitrary deadlines and unvalidated accuracy targets. Only label a milestone complete when code, tests or research artifacts demonstrate it.
