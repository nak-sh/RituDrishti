# RituDrishti (ऋतुदृष्टि)

**Knowing when the forecast can't be trusted.**
*Region by region, day by day, and why.*

AI-based forecast bust detection for medium-range weather forecasts.
Smart India Hackathon 2026 · Problem Statement 26079 · Ministry of Earth Sciences (MoES) / NCMRWF · Software · Smart Automation

---

## What it is

Medium-range models such as NCUM-G and NEPS-G are usually good, but they occasionally fail badly during fast-evolving systems: monsoon depressions, extreme rain, western disturbances, cyclones and heat waves. Forecasters normally find out about such a **bust** only after it has happened.

RituDrishti is a model-agnostic **"forecast of the forecast"** layer. For every region and every lead day from Day 1 to Day 10 it estimates:

- a **calibrated probability** that the forecast will bust,
- a **Forecast Confidence Index (FCI, 0–100)** and a **Trust Horizon** (the first day confidence drops below 65),
- the **hotspots** where and when the forecast is likely to fail,
- the **reasons**, using named meteorological drivers, counterfactual what-ifs and historical analogues, in English and Hindi.

> ### Honesty note: read this first
> This is a research prototype. **No live NCUM/NEPS/IMD data is connected.**
> All forecasts, observations, historical analogues and performance numbers come from a seeded, physically structured **synthetic** generator, and every screen carries a "Demo data: synthetic" badge.
> Metrics shown in the app are **computed at runtime** on held-out synthetic seasons; none are typed in. The three case studies (Cyclone Biparjoy, a Himalayan rain episode, a North India heat wave) are **illustrative synthetic scenarios**, not real back-tests.
> Do not use it for operational weather decisions. Real data plugs in through an adapter (see [Adapters](#adapters)).

---

## Features

| Area | What you get |
|---|---|
| **Command centre** | Government of India map coloured by FCI, Day 1–10 slider, hazard switch (Rain / Heat / Cyclone / Auto), 12-region × 10-day confidence matrix with Trust Horizon markers, ranked hotspots |
| **Explanation drawer** | FCI and band, calibrated bust probability, conformal error bound, top-3 drivers with risk share, counterfactual re-scoring, evidence chart, grounded English/Hindi narrative |
| **Historical analogues** | Nearest past situations with similarity, regime, forecast vs observation and realised error |
| **How reliable are we?** | Reliability diagram, Brier skill, ROC/PR-AUC, skill by lead and by BSISO phase, baseline comparison, PADI ablation, conformal coverage (including extremes), simulated model-upgrade drift and recalibration |
| **Case studies** | Three clearly labelled synthetic scenario timelines |
| **Decision intelligence** | Cost–loss slider that changes alert thresholds, alert list and held-out relative economic value |
| **Forecaster feedback** | One-click "Bust confirmed" / "False alarm" with a persistent queue |
| **Architecture / About** | Interactive five-layer diagram and the novelty features |
| **UX** | English/Hindi toggle, light/dark mode, responsive layout, local fonts, no external map tiles |

### Novelty

1. **Physics–AI Disagreement Index (PADI)**, an independent uncertainty signal (with an ablation view)
2. **Trust Horizon**, one decision number per region
3. Hazard-typed **bust labels**: relative (train-only 90th/95th percentile) plus impact triggers, with neighbourhood-scale error
4. **Calibrated probabilities** (isotonic per hazard and lead) and **conformal error bounds** with measured coverage
5. Flip-flop (cycle-consistency) and error-growth indices
6. Regime-aware behaviour (BSISO phase, season)
7. **Analogue engine** that returns past cases with realised errors
8. **Counterfactual explanations** computed by actually re-scoring the stack
9. **Self-verifying loop**: daily verification, online recalibration, drift alarm
10. **Cost–loss** personalised alert thresholds
11. **Grounded bilingual narrative** with an automatic number-consistency check
12. **Forecaster-in-the-loop** feedback

---

## Architecture

```
Inputs ──► Feature engine ──► Bust ML core ──► Trust layer ──► Delivery
 (adapter)   (physics-aware)   (3 tiers)       (honest odds)    (API + UI)
                                                     ▲               │
                                                     └── daily verification · online recalibration · drift alarm
```

| Layer | Implementation |
|---|---|
| 1. Inputs | `SyntheticAdapter` (active); `NCUMAdapter` stub for real NCMRWF data. Separate offline training lane and live inference lane |
| 2. Features | 20 physics-style features: spread, flip-flop, PADI, extremity (EFI-style), bimodality, jet/moisture/shear/soil proxies, regime, recent error, terrain, lead, region, model version |
| 3. Bust core | Tier 1: monotone **LightGBM** per hazard. Tier 2: nearest-neighbour analogues. Stacked by a logistic meta-learner. *BustFormer is roadmap only* |
| 4. Trust layer | Isotonic calibration per hazard and lead, one-sided quantile-head conformal bounds, exact TreeSHAP, counterfactuals, FCI and Trust Horizon, grounded narrative |
| 5. Delivery | FastAPI, React dashboard, forecaster feedback, scheduled verification |

**Monotone constraints** encode a physics rule: more ensemble spread, more cycle-to-cycle flip-flop or more physics–AI disagreement can never lower predicted bust risk.

**FCI** = 100 × (1 − calibrated P(bust)) of the dominant hazard. Bands: High ≥ 80, Moderate 65–80, Low 45–65, Very low < 45. **Trust Horizon** = first lead day with FCI < 65.

### Data protocol (leakage-safe)

| Block | Period |
|---|---|
| Train | 2019 – 21 Dec 2021 |
| Stacking | Jan – Jun 2022 |
| Calibration | Jul – Dec 2022 |
| Untouched test | 2023 – 2024 |

A 10-day embargo separates blocks. Bust thresholds are fitted on **train only** and applied unchanged afterwards. Splits are chronological, never random.

---

## Tech stack

**Backend:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn, LightGBM, scikit-learn, NumPy, pandas, PyArrow, joblib. Storage is MongoDB (Motor) if `MONGO_URL` is set, otherwise a JSON-file store, so no database is required.

**Frontend:** React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui (Radix), Recharts, d3-geo, i18next, Framer Motion, lucide-react. Inter and Manrope are bundled locally.

**Map:** bundled Government of India (NIC BharatMap) GeoJSON with 36 states/UTs, rendered as local SVG. No tile servers or third-party basemaps.

---

## Project structure

```
backend/
  server.py            FastAPI app and routes
  storage.py           MongoDB or JSON-file store for feedback and audit
  regions.py           12 forecast regions, hazards, synthetic init times
  adapters/            base contract, synthetic generator, NCUM stub
  features/  labels/   feature engine; bust labels (train-only thresholds)
  models/              HazardModel (LightGBM + analogues + stacking), training pipeline
  calibration/         isotonic per hazard and lead
  conformal/           adaptive conformal error bounds
  explain/             driver taxonomy, grounded narrative
  api/                 engine, verification metrics, cases, decision, online loop
  data/                bundled GeoJSON; generated models land here
frontend/
  src/pages/           Dashboard, Analogues, Reliability, Cases, Decision, Feedback, Architecture, About
  src/components/      IndiaMap, Matrix, ExplanationDrawer, charts, shell
  public/data/         bundled India GeoJSON and map provenance
scripts/               seed.py (train), make_zip.sh (export), prepare_map.py
tests/                 unit and API tests
```

---

## Quick start

### Prerequisites
Python 3.11+, Node 20+ and Yarn.

### 1. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd .. && python scripts/seed.py                         # generates data and trains models
cd backend && uvicorn server:app --port 8001
```
API docs: <http://localhost:8001/api/docs>

If you skip `seed.py`, the models train automatically on first start (this takes longer).

### 2. Frontend
```bash
cd frontend
printf "REACT_APP_BACKEND_URL=http://localhost:8001\nPORT=3000\n" > .env
yarn install
yarn start
```
Open <http://localhost:3000>. Both variables are required.

### Environment variables

| Variable | Where | Purpose |
|---|---|---|
| `REACT_APP_BACKEND_URL` | frontend | Backend base URL (the app adds `/api`) |
| `PORT` | frontend | Dev-server port |
| `MONGO_URL`, `DB_NAME` | backend, optional | Use MongoDB; if unset a JSON-file store is used |
| `CORS_ORIGINS` | backend, optional | Comma-separated origins (default: localhost:3000) |
| `WEBHOOK_CRON_SECRET` | backend, optional | Bearer token for the scheduled verification endpoint |
| `RITU_STORE_DIR` | backend, optional | Folder for the JSON-file store |

Never commit `.env` files.

---

## API

All routes are served under `/api` (and also without the prefix).

| Endpoint | Purpose |
|---|---|
| `GET /health` | Status, data mode, storage backend |
| `GET /v1/confidence?init=&hazard=&region=` | FCI, bust probability, conformal bound, Trust Horizon per region and lead |
| `GET /v1/bust-probability?init=&hazard=&lead=` | GeoJSON with calibrated values per state |
| `GET /v1/hotspots?init=&min_prob=&hazard=` | Ranked hotspots with onset, duration and peak |
| `GET /v1/explain?region=&lead=&lang=en\|hi` | Drivers, counterfactual, narrative, evidence, analogues |
| `GET /v1/analogs?region=&lead=&k=` | Nearest historical analogues |
| `GET /v1/verification?period=all\|2023\|2024` | Computed reliability, baselines, ablation, coverage, drift |
| `GET /v1/cases` | Synthetic scenario studies |
| `GET /v1/decision?cost_loss=` | Cost–loss thresholds, alerts, economic value |
| `GET` / `POST /v1/feedback` | Forecaster feedback queue |
| `GET /v1/verification-runs` | Scheduled verification audit |
| `POST /cron/verify` | Token-authenticated, idempotent daily verification |

Example (shape only; values are synthetic):
```json
{ "region": "konkan", "trust_horizon_day": 4,
  "leads": [{ "day": 5, "fci": 49, "p_bust": 0.51, "band": "Low", "hazard": "rain",
              "conformal_interval": [0, 42.1], "error_p90_class": "Severe" }] }
```

---

## Adapters

`backend/adapters/base.py` defines the contract: one row per init × region × lead × hazard, with units, availability time and version provenance, and no silent filling of missing values. To use real data, implement `NCUMAdapter.load()` (see `ncum_stub.py`) to supply licensed forecast grids, regional aggregation, valid times and observed truth. Open archives such as GEFSv12 reforecasts, TIGGE, IMD gridded rain/temperature and GPM IMERG are the intended substitutes when NCMRWF archives are not available. Training features must come from sources that have a historical archive, not only from live feeds.

---

## Testing

```bash
pip install -r backend/requirements.txt
pytest                              # unit tests
RITU_RUN_API_TESTS=1 pytest         # adds slow end-to-end API tests (needs models)
cd frontend && yarn build           # type-check and production build
```

Tests cover bust labels, calibration, conformal coverage, monotone constraints, narrative number-grounding, adapters and features, storage, map-boundary probes and the API contract.

---

## Map and boundaries

The map uses the official Government of India boundary data from NIC BharatMap (see `frontend/public/data/map-provenance.json`). Coverage probes confirm that Pakistan-occupied Kashmir, Gilgit-Baltistan and Aksai Chin fall inside Jammu & Kashmir and Ladakh, and that Arunachal Pradesh is shown in full. This is source and probe verification, **not Survey of India certification**. Sea regions are illustrative forecast boxes, not maritime boundaries. Check the Kashmir, Ladakh and Arunachal areas visually before any public use.

---

## Known limitations

- All data is synthetic; no operational NCMRWF validation exists.
- Conformal coverage is measured, not guaranteed, and can fail under distribution shift.
- Regional, terrain and monsoon-phase proxies are simplified.
- The PADI ablation removes the direct feature; correlated witnesses remain.
- Hindi covers navigation, core dashboard labels and evidence narratives, not the whole interface.
- BustFormer (spatio-temporal transformer) is not implemented.

## Roadmap

1. NCUM/NEPS adapters and the NCMRWF archive; GEFSv12/TIGGE pre-training
2. AI-model witnesses run from ERA5 initial dates for real PADI
3. BustFormer (regime-conditioned spatio-temporal network)
4. Shadow-mode run through a monsoon season; forecaster review
5. CAP alert export and cost–loss personalisation per user

---

## Credits

Built for Smart India Hackathon 2026 (PS 26079). Independent research prototype; not affiliated with or endorsed by MoES, NCMRWF or IMD.
