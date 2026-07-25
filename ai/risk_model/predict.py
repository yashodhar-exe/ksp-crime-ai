"""
Query-time inference for the risk model trained by train.py.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model" / "risk_model.joblib"

_bundle = None


class ModelNotTrainedError(RuntimeError):
    pass


def _ensure_loaded():
    global _bundle
    if _bundle is not None:
        return
    if not MODEL_PATH.exists():
        raise ModelNotTrainedError(
            "No risk model found. Run `python ai/risk_model/train.py` first "
            "(after dataset/generator/generate_dataset.py has produced dataset/processed/*.csv)."
        )
    import joblib

    _bundle = joblib.load(MODEL_PATH)


def is_available() -> bool:
    return MODEL_PATH.exists()


def predict_risk(
    *,
    case_category_id: int,
    crime_major_head_id: int,
    crime_minor_head_id: int,
    district_id: int,
    unit_type_id: int,
    incident_datetime: datetime | None,
) -> dict:
    """
    Returns {"risk_label": "Heinous" | "Non-Heinous", "risk_score": float}
    where risk_score is the model's predicted probability of the case
    turning out to be Heinous, based only on features known at FIR
    registration time (i.e. before an officer has manually assessed
    gravity). This is a triage signal for prioritizing review, not a
    replacement for that manual assessment.
    """
    _ensure_loaded()
    import pandas as pd

    model = _bundle["model"]
    encoders = _bundle["encoders"]
    feature_columns = _bundle["feature_columns"]
    categorical_features = _bundle["categorical_features"]

    dt = incident_datetime or datetime.utcnow()
    row = {
        "case_category_id": case_category_id,
        "crime_major_head_id": crime_major_head_id,
        "crime_minor_head_id": crime_minor_head_id,
        "district_id": district_id,
        "unit_type_id": unit_type_id,
        "incident_hour": dt.hour,
        "incident_dayofweek": dt.weekday(),
        "incident_month": dt.month,
    }
    X = pd.DataFrame([row])[feature_columns]

    for col in categorical_features:
        encoder = encoders[col]
        # unseen categories (e.g. a district id the model never saw) fall
        # back to the encoder's first known class rather than raising
        value = X.at[0, col]
        X.at[0, col] = encoder.transform([value])[0] if value in encoder.classes_ else 0

    risk_score = float(model.predict_proba(X)[0, 1])
    return {
        "risk_label": "Heinous" if risk_score >= 0.5 else "Non-Heinous",
        "risk_score": round(risk_score, 4),
    }
