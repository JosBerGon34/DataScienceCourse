# Operational Recipe & Debugging Guide: End-to-End ML Deployment (Module 10.1)

**Architecture:** Persistent Notebook Extractor (`joblib`) $\rightarrow$ Name-Aligned REST API (`Flask`) $\rightarrow$ Standalone Web Client (`HTML5/Vanilla JS`)

## 1. Repository Topology & Component Placement

Maintaining strict separation of concerns prevents data leakage, path breakages, and UI-to-model coupling. Every component lives in a dedicated directory relative to `ROOT_DIR`:

```
DataScienceCourse/
├── notebooks/
│   └── Ex10.1.ipynb                 # [Producer] Trains ImbPipeline & serializes 5 .joblib artifacts
├── models/                          # [Contract Storage] Gitignored binary artifacts
│   ├── best_happy_regressor.joblib  # Fitted pipeline (expects 8 exact named features)
│   ├── hotdeck_pools.joblib         # Country-level & global weighted imputation tables
│   ├── target_dist.joblib           # Sorted arrays for global, regional, and national percentiles
│   ├── knn_ref.joblib               # Scaled 5D reference matrix for multivariable KNN profiling
│   └── schema_meta.joblib           # Feature lists, ranges, labels, and country mappings
├── src/
│   └── app.py                       # [Middleware] Flask API: validation, imputation & inference
├── web/
│   └── HappyPredict.html            # [Consumer] Standalone UI with radial country selector
└── docs/                            # [GitHub Pages] Static documentation & simulation demo
```

## 2. Operational Recipe: Step-by-Step Execution Flow

### Phase A: The Persistent Extractor (`notebooks/Ex10.1.ipynb`)

1. **Dynamic Root Anchoring:** Resolve `ROOT_DIR = Path.cwd().parent` so artifact paths work identically across Linux, Windows, or CI environments.
    
2. **Asymmetric State Computation:** Compute `n_resp` (count of missing survey items per row) _before_ imputing missing values, ensuring `GroupKFold(groups="cntryfc")` isolates countries completely.
    
3. **Clean Serialization (`persist_all`):** Delete stale `.joblib` files before dumping new ones to prevent schema drift. Verify `best_pipe.named_steps["model"].feature_names_in_` contains the exact 8 expected features (`lrscale`, `rlgdgr`, `agea`, `gndr`, `hhmmb`, `mnactic`, `regionfc`, `n_resp`).
    

### Phase B: The Inference Middleware (`src/app.py`)

1. **Portable Path Resolution:** Anchor `ROOT = Path(__file__).resolve().parents[1]` and load all 5 `.joblib` artifacts at startup inside a `try/except` block.
    
2. **Unified Entrypoint & CORS:** Enable `CORS(app)` and serve `HappyPredict.html` directly at `GET /` via `send_from_directory(ROOT / "web", "HappyPredict.html")`, alongside `GET /health` and `POST /predict`.
    
3. **Inference Pipeline per Request (`POST /predict`):**
    
    - Count `null` fields in the incoming JSON payload to compute `n_resp` dynamically.
        
    - Impute missing values using country-specific weighted **Hot-Deck** sampling (falling back to the global pool if country is omitted).
        
    - Construct a 1-row `pd.DataFrame` ordered strictly by `model.feature_names_in_` (never by positional lists).
        
    - Execute `pipe.predict(row_df)` and compute the 4 reference percentiles (Global, Macro-Region, Country, and 5D KNN).
        

### Phase C: The Web Client (`web/HappyPredict.html`)

1. **Health Handshake on Load:** On `DOMContentLoaded`, fire `GET /health`. If HTTP `200` is returned, switch the status badge to **`LIVE BACKEND`** (green); otherwise, fall back gracefully to **`SIMULATION MODE`** (amber).
    
2. **State Synchronization:** Keep sliders, numeric inputs, and _"No response"_ checkboxes synchronized. Checking _"No response"_ disables the control and sends `null` in the JSON payload.
    
3. **Radial Country Selector:** Maps the selected ISO code (`ES`, `HU`, etc.) to `cntryfc` (for national hot-deck/percentiles) and `regionfc` (macro-regional model input).
    

## 3. Component-by-Component Debugging Playbook

|   |   |   |   |
|---|---|---|---|
|**Layer**|**Symptom / Failure Mode**|**Root Cause**|**Diagnostic & Fix**|
|**Notebook Extractor**|`n_resp` missing in `feature_names_in_` after updating `DatasetSpec`.|Stale `.joblib` file on disk was not overwritten or kernel cached old state.|Delete `models/*.joblib`, restart kernel, re-run `persist_all()`, and inspect `joblib.load(...).named_steps["model"].feature_names_in_`.|
|**Notebook Extractor**|`ValueError: feature_names mismatch` during inference.|Grouping column (`cntryfc`) leaked into `X_train` or column order shifted.|Verify `excluded = {spec.target, spec.group}` in `DatasetSpec` and always pass a named `pd.DataFrame` to `.predict()`.|
|**Flask Backend**|`ModuleNotFoundError: No module named 'flask_cors'`|Running global Python instead of `.venv-core`, or package missing in profile.|Activate `.venv-core`, run `pip install flask flask-cors`, and pin both inside `requirements/ReqJupML.txt`.|
|**Flask Backend**|`404 Not Found` at `http://127.0.0.1:5000`|Flask only exposed `/health` and `/predict`, with no root `/` route.|Add `@app.route("/")` returning `send_from_directory(ROOT / "web", "HappyPredict.html")`.|
|**HTML / JS Client**|Radial wheel & sliders do not render inside JupyterLab tab.|JupyterLab's security sandbox blocks `<script>` execution in untrusted HTML.|Click **`Trust HTML`** in the top toolbar of the JupyterLab viewer tab, or open via Flask URL.|
|**HTML / JS Client**|Badge stuck on `SIMULATION MODE` despite Flask running.|Port mismatch (`5000`), CORS block, or `model_loaded: false` in `/health`.|Open DevTools (`F12` $\rightarrow$ Network/Console) and inspect the raw JSON response from `http://127.0.0.1:5000/health`.|

## 4. Quick Verification Checklist (Pre-Commit)

1. **Cold Artifact Check:** Run `python -c "import joblib; m=joblib.load('models/best_happy_regressor.joblib'); print(list(m.named_steps['model'].feature_names_in_))"` from root.
    
2. **Server Boot:** Run `python src/app.py` inside `.venv-core` and confirm `Running on http://127.0.0.1:5000`.
    
3. **Non-Response Test:** Toggle two _"No response"_ checkboxes in the UI, click **Predecir**, and verify `n_resp: 2` updates both the score and percentiles cleanly.

### How to Test & Run Module 10.1 on GitHub Pages (`main` + `/docs`)

Yes, you can host and run the interactive frontend directly from **GitHub Pages** (`[https://josbergon34.github.io/DataScienceCourse/](https://josbergon34.github.io/DataScienceCourse/)...`), with one important architectural distinction:

- **What GitHub Pages executes:** GitHub Pages is a **static file server** (HTML, CSS, JS, Markdown). It will render `HappyPredict.html` with full interactivity—including the radial pizza selector, sliders, checkboxes, and real-time predictions—automatically activating **`SIMULATION MODE`** because GitHub Pages does not run a Python/Flask backend server.
    
- **How to publish it inside `/docs` on `main`:**
    
    1. Copy `web/HappyPredict.html` into your GitHub Pages directory (for example, `docs/apps/HappyPredict.html` or `docs/HappyPredict.html`).
        
    2. Add a direct link to it in your `docs/index.md` table for Module 10.1 (e.g., `[Live Demo (Simulation Mode)](HappyPredict.html)`).
        
    3. Commit and push to `main`:

```bash
mkdir -p docs/apps
     cp web/HappyPredict.html docs/apps/HappyPredict.html
     git add docs/
     git commit -m "feat(docs): publish Module 10.1 interactive viewer to GitHub Pages"
     git push origin main
```

Wait 1–2 minutes for GitHub Pages to build and visit `[https://josbergon34.github.io/DataScienceCourse/apps/HappyPredict.html](https://josbergon34.github.io/DataScienceCourse/apps/HappyPredict.html)` (press `Ctrl + F5` to bypass browser cache).