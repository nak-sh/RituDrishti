# RituDrishti PRD

## Original problem statement
Build a working national-level SIH 2026 PS 26079 prototype for a model-agnostic forecast-of-the-forecast assurance layer on NCUM-G / NEPS-G. Required: physically structured synthetic data with honest badges, Government of India boundary map, per-region Day 1–10 calibrated bust probabilities, FCI, Trust Horizon, hotspots, explanations, historical analogues, computed verification, case studies, cost–loss decisions, feedback, bilingual narratives, five-layer architecture, tests and downloadable code. User explicitly chose Government of India map sources and autonomous milestone progression. User subsequently paused execution and requested the ZIP immediately.

## Personas
- National and regional forecasters investigating medium-range forecast bust risk.
- Disaster-management and dam-operation decision makers comparing cost and loss.
- Hackathon evaluators inspecting scientific provenance, architecture and reproducibility.

## Architecture decisions
- React + TypeScript + Vite, Tailwind/shadcn primitives, Recharts, d3-geo, i18next; bundled local fonts and map.
- FastAPI/Pydantic, LightGBM, sklearn isotonic/logistic/nearest-neighbours, exact LightGBM TreeSHAP, quantile-head conformal intervals.
- Generated parquet/joblib files; MongoDB for forecaster feedback and verification audit.
- Source adapters explicitly separate synthetic and unconnected NCUM integrations.
- NIC BharatMap government GeoJSON with 36 states/UTs; no tiles or third-party basemap.
- Chronological training/stack/calibration/test blocks and ten-day embargo.

## Core requirements
- Never misrepresent synthetic forecasts, metrics or scenario back-tests as operational evidence.
- Every metric computed from held-out synthetic records; no hard-coded performance claims.
- Explain forecast bust risk, not replace an operational hazard warning service.
- Package checkpoint ZIP excluding private environment values, dependencies, caches and large generated datasets.

## Implemented — 2026-09-30
- M1–M2 data/model foundation and core API.
- M3 command dashboard, map, matrix, filters and hotspots.
- M4 evidence drawer, TreeSHAP, counterfactuals, EN/HI grounded narratives and analogue gallery.
- M5 verification charts, baselines, ablation, empirical intervals, drift experiment and scheduled verification code.
- M6 cases, decisions, feedback, architecture and novelty pages.
- Partial M7: production build passes; desktop/mobile dashboard and drawer tested; close-state crash fixed.
- Export requested immediately by user before comprehensive testing; CURRENT_CHECKPOINT.md records limitations.

## Prioritised backlog
### P0
- Finish comprehensive testing-agent pass and unit tests for labels, monotonicity, calibration, coverage and numeric grounding.
- Verify scheduled endpoint auth/idempotency/outcome changes and all core API/user flows.
- Put full synthetic-data disclosure persistently in the header on all screens.
### P1
- Clean-machine one-command runner, .env examples, complete README, architecture notes and three-minute demo script.
- Verify every page and dark mode at mobile/desktop; fix findings.
- Persist online calibrator state across worker restarts.
### P2
- Broaden Hindi UI translation; improve scientific proxies and regional aggregation.
- Real licensed forecast/truth adapters and multi-fold seasonal walk-forward studies.
- BustFormer remains explicitly roadmap-only.

## Next action
Deliver current ZIP immediately. Resume unfinished M7 only if requested.