"""
Module 10.1: Flask REST API for HappyPredict.
Loads 5 persisted artifacts, validates by feature name, imputes nulls,
predicts, and returns 4-level percentiles.
"""
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Dynamic path resolution ---
ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "models" / "best_happy_regressor"

# --- 2. Load artifacts at startup ---
app = Flask(__name__)
CORS(app)

try:
    pipe         = joblib.load(f"{M}.joblib")
    impute_table = joblib.load(f"{M}_impute.joblib")
    target_dist  = joblib.load(f"{M}_target_dist.joblib")
    knn_data     = joblib.load(f"{M}_knn.joblib")
    encodings    = joblib.load(f"{M}_encodings.joblib")
    MODEL_LOADED = True
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    MODEL_LOADED = False

model_step = pipe.named_steps["model"] if MODEL_LOADED else None
EXPECTED_FEATURES = list(model_step.feature_names_in_) if MODEL_LOADED else []


# --- 3. GET /health ---
@app.route("/health", methods=["GET"])
def health():
    if not MODEL_LOADED:
        return jsonify({"status": "error", "message": "Model not loaded"}), 503
    return jsonify({
        "status": "ok",
        "model_type": type(model_step).__name__,
        "expected_features": EXPECTED_FEATURES,
        "n_features": len(EXPECTED_FEATURES),
    })


# --- 4. POST /predict ---
@app.route("/predict", methods=["POST"])
def predict():
    if not MODEL_LOADED:
        return jsonify({"error": "Model not loaded"}), 503

    payload = request.get_json(silent=True)
    if payload is None or not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    # --- Translate frontend names to factorized codes ---
    cntry_name = payload.get("cntry")
    if cntry_name and cntry_name in encodings["cntry_to_fc"]:
        payload["cntryfc"]  = encodings["cntry_to_fc"][cntry_name]
        payload["regionfc"] = encodings["cntry_to_region"][cntry_name]

    # --- Count nulls → n_resp ---
    n_resp = 0
    for col in EXPECTED_FEATURES:
        if col == "n_resp":
            continue
        if payload.get(col) is None:
            n_resp += 1
    payload["n_resp"] = n_resp

    # --- Hot-deck imputation of nulls ---
    cntryfc  = payload.get("cntryfc")
    regionfc = payload.get("regionfc")
    rng = np.random.default_rng()

    for col in EXPECTED_FEATURES:
        if payload.get(col) is None:
            # Try country-level, then region-level, then global
            key = (cntryfc, col)
            if key in impute_table:
                vals, probs = impute_table[key]
            else:
                key = (None, col)
                vals, probs = impute_table[key]
            payload[col] = float(rng.choice(vals, p=probs))

    # --- Validate: all features present and numeric ---
    missing = [c for c in EXPECTED_FEATURES if c not in payload]
    if missing:
        return jsonify({"error": "Missing features", "missing": missing}), 400

    invalid = []
    for c in EXPECTED_FEATURES:
        try:
            payload[c] = float(payload[c])
            if np.isnan(payload[c]):
                invalid.append(c)
        except (ValueError, TypeError):
            invalid.append(c)
    if invalid:
        return jsonify({"error": "Invalid types", "invalid": invalid}), 400

    # --- Build 1-row DataFrame ordered by feature_names_in_ ---
    X = pd.DataFrame([[payload[c] for c in EXPECTED_FEATURES]], columns=EXPECTED_FEATURES)

    # --- Predict ---
    pred = float(pipe.predict(X)[0])

    # --- Percentiles (4 levels) ---
    pred_rounded = round(pred, 1)

    # Global
    p_global = np.searchsorted(np.sort(target_dist["global"]), pred) / len(target_dist["global"])

    # Region
    p_region = 0.5
    if regionfc is not None and int(regionfc) in target_dist.get("region", {}):
        arr = np.sort(target_dist["region"][int(regionfc)])
        p_region = np.searchsorted(arr, pred) / len(arr)

    # Country
    p_country = 0.5
    if cntryfc is not None and int(cntryfc) in target_dist.get("country", {}):
        arr = np.sort(target_dist["country"][int(cntryfc)])
        p_country = np.searchsorted(arr, pred) / len(arr)

    # Multivariable (KNN)
    p_multivar = 0.5
    numeric_cols = knn_data["numeric_cols"]
    if all(c in payload for c in numeric_cols):
        x_user = np.array([payload[c] for c in numeric_cols], dtype=float)
        x_norm = (x_user - knn_data["X_mean"]) / knn_data["X_std"]
        _, indices = knn_data["tree"].query(x_norm, k=50)
        neighbors = knn_data["happy"][indices]
        p_multivar = np.searchsorted(np.sort(neighbors), pred) / len(neighbors)

    return jsonify({
        "prediction": pred_rounded,
        "percentile_global":    round(p_global * 100),
        "percentile_region":    round(p_region * 100),
        "percentile_country":   round(p_country * 100),
        "percentile_multivar":  round(p_multivar * 100),
        "n_resp": n_resp,
        "features_used": EXPECTED_FEATURES,
    })


# --- 5. Entrypoint ---
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)