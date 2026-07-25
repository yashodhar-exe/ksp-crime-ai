"""
Model 1 (per the hackathon reference notes): Crime Risk Prediction.

Trains a small XGBoost classifier to predict whether a newly-registered
case is likely to be "Heinous" (GravityOffence) — using only features
known at FIR registration time (crime category, crime head/sub-head,
district, station type, and time-of-day/week), i.e. *before* an officer
has manually assessed gravity. This is meant to flag cases for priority
review, not to replace human judgement.

Usage:
    python ai/risk_model/train.py

Reads dataset/processed/*.csv (run dataset/generator/generate_dataset.py
first). Writes ai/risk_model/model/risk_model.joblib (bundles the fitted
XGBoost model + the label encoders + the feature column order, so
predict.py doesn't need to duplicate any preprocessing logic).
"""
from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

DATASET_DIR = Path(__file__).parent.parent.parent / "dataset" / "processed"
MODEL_PATH = Path(__file__).parent / "model" / "risk_model.joblib"

CATEGORICAL_FEATURES = [
    "case_category_id", "crime_major_head_id", "crime_minor_head_id",
    "district_id", "unit_type_id",
]
NUMERIC_FEATURES = ["incident_hour", "incident_dayofweek", "incident_month"]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET_COLUMN = "is_heinous"


def _build_training_frame() -> pd.DataFrame:
    cases = pd.read_csv(DATASET_DIR / "case_master.csv")
    unit = pd.read_csv(DATASET_DIR / "unit.csv")

    df = cases.merge(
        unit[["unit_id", "district_id", "type_id"]].rename(columns={"type_id": "unit_type_id"}),
        left_on="police_station_id", right_on="unit_id", how="left",
    )

    incident = pd.to_datetime(df["incident_from_date"], errors="coerce")
    df["incident_hour"] = incident.dt.hour.fillna(-1).astype(int)
    df["incident_dayofweek"] = incident.dt.dayofweek.fillna(-1).astype(int)
    df["incident_month"] = incident.dt.month.fillna(-1).astype(int)

    df[TARGET_COLUMN] = (df["gravity_offence_id"] == 1).astype(int)  # 1 == "Heinous" (seeded in gravity_offence.csv)

    for col in CATEGORICAL_FEATURES:
        df[col] = df[col].fillna(-1).astype(int)

    return df[FEATURE_COLUMNS + [TARGET_COLUMN]].dropna()


def train() -> None:
    print("Building training frame from dataset/processed/ ...")
    df = _build_training_frame()
    print(f"  {len(df)} rows, heinous rate = {df[TARGET_COLUMN].mean():.1%}")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN]

    encoders: dict[str, LabelEncoder] = {}
    for col in CATEGORICAL_FEATURES:
        enc = LabelEncoder()
        X[col] = enc.fit_transform(X[col])
        encoders[col] = enc

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    print(f"\nTest accuracy: {accuracy_score(y_test, preds):.3f}")
    print(f"Test ROC-AUC:  {roc_auc_score(y_test, probs):.3f}")
    print(classification_report(y_test, preds, target_names=["Non-Heinous", "Heinous"]))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "model": model,
        "encoders": encoders,
        "feature_columns": FEATURE_COLUMNS,
        "categorical_features": CATEGORICAL_FEATURES,
    }, MODEL_PATH)
    print(f"\nSaved model -> {MODEL_PATH}")


if __name__ == "__main__":
    train()
