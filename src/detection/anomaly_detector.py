import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models", "anomaly_model.pkl")


# ---------------- LOAD MODEL ----------------
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ AI model loaded successfully.")
        return model

    except Exception as e:
        print("❌ Model loading failed:", e)
        return None


# ---------------- PREPROCESS ----------------
def preprocess(features, model):
    try:
        if hasattr(model, "feature_names_in_"):
            expected = list(model.feature_names_in_)

            for col in expected:
                if col not in features.columns:
                    features[col] = 0

            features = features[expected]

        return features

    except Exception as e:
        print("[ERROR] Feature preprocessing failed:", e)
        return pd.DataFrame()


# ---------------- DETECT ----------------
def detect(model, features):

    if model is None or features.empty:
        return [], []

    try:
        # Step 1: preprocess
        features = preprocess(features, model)

        if features.empty:
            return [], []

        # Step 2: predict
        predictions = model.predict(features)

        # Step 3: anomaly score
        scores = model.decision_function(features)

        # 🔥 ALWAYS return BOTH
        return list(predictions), list(scores)

    except Exception as e:
        print("[ERROR] Detection failed:", e)
        return [], []