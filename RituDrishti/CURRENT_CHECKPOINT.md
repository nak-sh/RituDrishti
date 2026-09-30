# RituDrishti — current code checkpoint

Export requested by the user before final milestone completion.

## Implemented
- React/TypeScript/Vite dashboard with government-source bundled India GeoJSON, map modes, hazard switching, lead slider, confidence matrix and hotspots.
- Reproducible synthetic data generator, bust labels, monotone LightGBM models, logistic stacking, isotonic calibration, nearest-neighbour analogues and conformal error intervals.
- Explanation drawer, exact TreeSHAP contributions, actual counterfactual re-scoring and grounded English/Hindi narratives.
- Computed reliability/baseline/PADI-ablation views, synthetic scenario case studies, cost–loss decisions, persistent feedback and interactive architecture/about pages.
- Scheduled verification endpoint and configuration, with authentication and idempotency logic.

## Verified so far
- TypeScript and Vite production build passed.
- Core confidence API and explanation drawer exercised in the running preview.
- Dashboard, map, matrix and drawer checked at 1920×800 and 390×844; no horizontal overflow in those checks.
- Drawer-close crash fixed and rechecked.
- Government map has 36 states/UTs. Coverage checks pass for PoK, Gilgit-Baltistan, Aksai Chin and Arunachal Pradesh. This is source/probe/visual verification, not official Survey of India certification.

## Not yet completed or fully verified
- M7 comprehensive automated/unit tests, full cross-page interaction and dark-mode checks.
- Scheduler authentication, idempotency and outcome-update end-to-end verification.
- One-command clean-machine setup, final architecture documentation and three-minute presentation script.
- All-screen, always-visible synthetic badge polish; current footer/drawer badges exist, but the header currently uses a shorter demo-workspace indicator.
- Online calibration snapshot persistence: updates are in-memory; audit records persist.
- Full UI Hindi translation beyond navigation, core dashboard labels and evidence narratives.

## Recreating generated files
- Trained `.joblib` files and large `.parquet` archives are intentionally excluded.
- Install backend dependencies, then run `python scripts/seed.py` from the project root to regenerate them.
- Install frontend dependencies with `yarn install`; `yarn start` runs Vite and `yarn build` builds it.
- Supply private backend/frontend `.env` files; they are intentionally excluded from the ZIP.
- Frontend variables: `REACT_APP_BACKEND_URL` and `PORT`.
- Backend variables: `MONGO_URL`, `DB_NAME`, `CORS_ORIGINS`, and a random `WEBHOOK_CRON_SECRET` for scheduled calls.
- The hosted preview uses supervisor to run FastAPI at 0.0.0.0:8001 and Vite at the configured frontend port. The same-origin host must route `/api` to FastAPI and other paths to the frontend.

## Honesty notes
No live NCUM/NEPS/IMD integration is connected. All forecasts, observed outcomes, historical analogue records and model-performance metrics are synthetic. Metrics are computed rather than invented. The three real-world event names describe illustrative synthetic scenarios. BustFormer is roadmap-only. Empirical conformal coverage is not an unconditional guarantee under drift.

See CHANGELOG.md for milestone details and frontend/public/data/map-provenance.json for the government boundary source and retrieval limitations.