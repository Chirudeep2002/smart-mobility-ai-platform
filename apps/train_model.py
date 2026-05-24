# apps/train_model.py

import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier, XGBRegressor


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "trips_with_weather_best_mode_cleaned.csv"
)

def main():
    df = pd.read_csv(DATA_PATH)

    # ----------------------- COST MODELS -----------------------
    cost_features = [
        "taxi_avg_duration",
        "scooter_avg_duration",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "windspeed_10m",
        "cloudcover",
        "peak_hour",
    ]

    taxi_model = XGBRegressor(
        n_estimators=400, learning_rate=0.05,
        max_depth=6, subsample=0.9, colsample_bytree=0.9, random_state=42
    )
    taxi_model.fit(df[cost_features], df["taxi_avg_cost"])
    joblib.dump(taxi_model, "taxi_cost_model.pkl")

    scooter_model = XGBRegressor(
        n_estimators=400, learning_rate=0.05,
        max_depth=6, subsample=0.9, colsample_bytree=0.9, random_state=42
    )
    scooter_model.fit(df[cost_features], df["scooter_avg_cost"])
    joblib.dump(scooter_model, "scooter_cost_model.pkl")

    # ----------------------- MODE CLASSIFIER -----------------------
    mode_features = [
        "taxi_avg_cost",
        "scooter_avg_cost",
        "taxi_avg_duration",
        "scooter_avg_duration",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "windspeed_10m",
        "cloudcover",
        "peak_hour",
    ]

    X = df[mode_features]
    y = df["best_mode_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train_res)
    X_test_scaled = scaler.transform(X_test)

    model = XGBClassifier(
        n_estimators=350,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train_scaled, y_train_res)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    print("\n==== MODE MODEL PERFORMANCE ====")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print("===============================\n")

    joblib.dump(model, "best_xgboost_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    with open("feature_cols.json", "w") as f:
        json.dump(mode_features, f, indent=2)

    print("Training completed successfully!")


if __name__ == "__main__":
    main()
