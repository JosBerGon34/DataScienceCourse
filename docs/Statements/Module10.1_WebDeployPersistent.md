🟢 < Module 10.1 > Model Serialization, Name-Aligned Flask REST API & Standalone HTML/JS Client

### 🎯 Context & Objectives

A Machine Learning pipeline living inside a Jupyter Notebook delivers zero operational value until external systems or end-users can query it reliably. In traditional prototypes (such as monolithic Streamlit scripts), model inference is tightly coupled to the UI and often suffers from positional array mismatches (`ValueError: feature_names mismatch`) when different target models require distinct subsets of selected features[.

In this exercise, you will decouple your validated predictive model from Module 9 into a **client-server production architecture**
1. Serialize your trained `ImbPipeline` artifact using portable relative paths (`pathlib`).
2. Build a lightweight **Flask REST API** (`src/app.py`) that validates incoming JSON payloads **by exact feature name** against `model.feature_names_in_`.
3. Pair it with a standalone **HTML5/Vanilla JavaScript client** (`web/index.html`) featuring numeric inputs/sliders, asynchronous `fetch()` calls, and a graceful client-side simulation fallback mode.

---

### 📑 Exercise Instructions

#### 1. Syntactic / Algorithmic Level (Artifact Serialization & Name-Aligned Flask API)

- **Portable Pipeline Serialization (`joblib` & `pathlib`):**
    - From your Module 9 notebook, export your best trained `ImbPipeline` (e.g., Hybrid Logistic Regression or Gradient Boosting) to `models/best_ess_pipeline.joblib` using `joblib.dump()`.
    - Resolve all filesystem paths dynamically via `pathlib.Path(__file__).resolve().parents[1]`—zero hardcoded Windows or Linux user paths.
    - Ensure `flask` and `flask-cors` are available in your active `.venv-core` environment (extending `requirements/ReqJupML.txt`).

- **RESTful Inference Contract (`src/app.py`):**
    - Enable CORS (`flask_cors.CORS(app)`) so a locally opened `web/index.html` file in Chromium can communicate with `http://127.0.0.1:5000` without browser origin blocks.
    - Expose `GET /health` returning the loaded model status, estimator class name, and the exact ordered list of expected input features (`model.feature_names_in_`).
    - Expose `POST /predict` accepting a JSON object of feature key-value pairs:
        - **Strict Feature-Name Validation:** Check that all keys in `model.feature_names_in_` exist in the incoming JSON and contain valid numeric values. If any key is missing or invalid, return HTTP `400 Bad Request` with a descriptive JSON error listing `missing_features` or `invalid_types`
        - **DataFrame Construction:** Build a 1-row `pd.DataFrame` ordered strictly by `list(model.feature_names_in_)` (never by raw positional lists) before calling `.predict()` and `.predict_proba()`.
        - Return HTTP `200 OK` with a structured JSON payload (`prediction`, `probability`, `label`, `features_used`).

---

#### 2. Applied / Data Level (Standalone HTML/JS Web Client & API Testing)

- **Interactive Parameter Controls (`web/index.html`):**
    - Build a clean, responsive HTML5 interface with sliders (`<input type="range">`) and numeric inputs (`<input type="number">`) matching your trained model's feature contract (e.g., `lrscale`, `institutional_trust_index`, `gdpcapitapct`, `inflationpct`, `unemploymentpct`, `macro_cluster`).
    - Display live numeric readouts next to every slider and provide a "Reset Defaults" button.

- **Asynchronous `fetch()` & Graceful Fallback Mode:**
    - Send an asynchronous `POST` request (`Content-Type: application/json`) to `http://127.0.0.1:5000/predict` when the user submits or adjusts parameters.
    - Wrap the network call in `try / catch`: when the Flask server responds, display the real model probability with a **`LIVE BACKEND`** badge; if unreachable (e.g., static preview on GitHub Pages), execute a transparent client-side heuristic and display a **`SIMULATION MODE`** warning badge.

- **End-to-End Integration Verification:**
    - Verify the API from terminal (`curl`) or a test script (`requests`) demonstrating:
        1. A valid JSON payload returning HTTP `200` and probability scores.
        2. A malformed JSON payload (omitting one required feature) returning HTTP `400` with the exact missing column name.

---

### 🌐 Official References & Documentation

- **Flask Quickstart & Request Parsing:** [Flask Official Documentation](https://flask.palletsprojects.com/en/latest/quickstart/)
- **Scikit-Learn Model Persistence:** [Model Persistence with Joblib](https://scikit-learn.org/stable/model_persistence.html)
- **Python `pathlib` Standard Library:** [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
- **MDN Fetch API Guide:** [Using the Fetch API (JavaScript)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

---

### 📚 Recommended Manuals & CheatSheets

- **Serving ML Models in Production:** *Designing Machine Learning Systems (Chip Huyen)* — Chapter 7 (Model Deployment and Prediction Service).
- **Web APIs & JSON Contracts:** *Flask Web Development (Miguel Grinberg)* — Chapter 14 (Application Programming Interfaces).

💻 **Your Challenge:** Serialize your best Module 9 pipeline, implement the name-validated Flask server (`src/app.py`) and standalone client (`web/index.html`), test both `200` and `400` HTTP responses, and share your solution here for code review! 🚀🌐