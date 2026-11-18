# src/app.py — Architectural Blueprint (Pseudocode)

# 1. IMPORTS & DYNAMIC PATH RESOLUTION
#    - Import Path from pathlib, Flask, request, jsonify, CORS, joblib, pandas
#    - Resolve ROOT_DIR = Path(__file__).resolve().parents[1]
#    - Define MODEL_PATH = ROOT_DIR / "models" / "best_ess_pipeline.joblib"

# 2. APP INITIALIZATION & MODEL LOADING
#    - Initialize Flask app and enable CORS(app)
#    - Load serialized pipeline via joblib.load(MODEL_PATH) inside try/except
#    - Extract EXPECTED_FEATURES = list(model.feature_names_in_)

# 3. ROUTE: GET /health
#    - Return JSON (HTTP 200 if loaded, 503 if model missing):
#        {
#            "status": "ok",
#            "model_type": type(model).__name__,
#            "expected_features": EXPECTED_FEATURES
#        }

# 4. ROUTE: POST /predict
#    - Parse JSON body: payload = request.get_json(silent=True)
#    - Guard 1: If payload is None or not a dict -> return 400 ("Invalid JSON payload")
#    - Guard 2 (Name Alignment):
#        * Find missing = [col for col in EXPECTED_FEATURES if col not in payload]
#        * If missing is not empty -> return 400 with {"error": "Missing features", "missing": missing}
#    - Guard 3 (Type Coercion & NaN Check):
#        * Convert each expected feature value to float(payload[col]) inside try/except (ValueError, TypeError)
#        * If conversion fails or value is NaN -> return 400 with offending column name
#    - Inference:
#        * Build 1-row DataFrame strictly ordered by EXPECTED_FEATURES:
#          input_df = pd.DataFrame([{col: float(payload[col]) for col in EXPECTED_FEATURES}], columns=EXPECTED_FEATURES)
#        * pred_class = int(model.predict(input_df)[0])
#        * pred_proba = float(model.predict_proba(input_df)[0, 1]) (if hasattr(model, "predict_proba"))
#    - Return JSON (HTTP 200):
#        {
#            "prediction": pred_class,
#            "probability": round(pred_proba, 4),
#            "features_used": EXPECTED_FEATURES
#        }

# 5. ENTRYPOINT
#    - If __name__ == "__main__": app.run(host="127.0.0.1", port=5000, debug=True)