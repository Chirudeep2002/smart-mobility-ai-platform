import os
import json
import joblib
import pandas as pd
import requests
from datetime import datetime

from autocomplete import geocode_address
from google_map import get_route
from utils import get_weather, compute_danger_score, apply_rules


# =========================================================
# LOAD ML FILES
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

best_model = joblib.load(
    os.path.join(BASE_DIR, "best_xgboost_model.pkl")
)

taxi_model = joblib.load(
    os.path.join(BASE_DIR, "taxi_cost_model.pkl")
)

scooter_model = joblib.load(
    os.path.join(BASE_DIR, "scooter_cost_model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "scaler.pkl")
)

with open(os.path.join(BASE_DIR, "feature_cols.json")) as f:
    FEATURE_COLS = json.load(f)


# =========================================================
# PEAK HOUR DETECTION
# =========================================================

def is_peak_hour():
    hour = datetime.now().hour

    # Morning + Evening traffic
    if (7 <= hour <= 10) or (16 <= hour <= 19):
        return 1

    return 0


# =========================================================
# MAIN PREDICTOR
# =========================================================

def suggest_mode(origin, destination, user_preference="Balanced"):

    # -----------------------------------------------------
    # GEOCODING
    # -----------------------------------------------------
    lat_o, lon_o = geocode_address(origin)
    lat_d, lon_d = geocode_address(destination)

    if not lat_o or not lat_d:
        return {"error": "Unable to fetch coordinates."}

    # -----------------------------------------------------
    # GOOGLE ROUTE
    # -----------------------------------------------------
    route = get_route(origin, destination)

    if route:
        distance_km, route_duration_min, polyline = route
    else:
        return {"error": "Unable to fetch route."}

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------
    weather = get_weather(lat_o, lon_o)

    danger_score = compute_danger_score(weather)

    # -----------------------------------------------------
    # ESTIMATE DURATIONS
    # -----------------------------------------------------
    taxi_duration = route_duration_min

    # Scooters slightly slower
    scooter_duration = round(route_duration_min * 1.25, 2)

    # -----------------------------------------------------
    # PEAK HOUR
    # -----------------------------------------------------
    peak_hour = is_peak_hour()

    # -----------------------------------------------------
    # ML FEATURES FOR COST MODELS
    # -----------------------------------------------------
    cost_features = pd.DataFrame([{
        "taxi_avg_duration": taxi_duration,
        "scooter_avg_duration": scooter_duration,
        "temperature_2m": weather["temp"],
        "relative_humidity_2m": weather["humidity"],
        "precipitation": weather["rain"],
        "windspeed_10m": weather["wind"],
        "cloudcover": weather["clouds"],
        "peak_hour": peak_hour,
    }])

    # -----------------------------------------------------
    # RAW ML PREDICTIONS
    # -----------------------------------------------------

    taxi_cost_raw = float(
    taxi_model.predict(cost_features)[0]
    )

    scooter_cost_raw = float(
    scooter_model.predict(cost_features)[0]
    )

    # =====================================================
    # RULE-BASED PRICING ENGINE
    # =====================================================

    taxi_base = 4
    scooter_base = 2

    taxi_per_km = 2.0
    scooter_per_km = 0.6

    taxi_per_min = 0.35
    scooter_per_min = 0.10

    weather_multiplier = 1

    if weather["weather"] in ["Rain", "Thunderstorm"]:
        weather_multiplier = 1.25

    peak_multiplier = 1.15 if peak_hour else 1

    # Rule-based Taxi Cost
    rule_taxi_cost = round(
    (
        taxi_base
        + (distance_km * taxi_per_km)
        + (taxi_duration * taxi_per_min)
    )
    * weather_multiplier
    * peak_multiplier,
    2
    )

# Rule-based Scooter Cost
    rule_scooter_cost = round(
    (
        scooter_base
        + (distance_km * scooter_per_km)
        + (scooter_duration * scooter_per_min)
    )
    * peak_multiplier,
    2
    )

# =====================================================
# HYBRID COST FUSION
# =====================================================

    def hybrid_price(ml_price, rule_price):

    # ML prediction too high
        if ml_price > (rule_price * 2.5):

            return round(
            (rule_price * 0.85)
            + (ml_price * 0.15),
            2
        )

    # ML prediction too low
        elif ml_price < (rule_price * 0.5):

            return round(
            (rule_price * 0.90)
            + (ml_price * 0.10),
            2
        )

    # Normal case
        else:

            return round(
            (ml_price * 0.4)
            + (rule_price * 0.6),
            2
            )

# =====================================================
# FINAL HYBRID PRICES
# =====================================================

    taxi_cost = hybrid_price(
    taxi_cost_raw,
    rule_taxi_cost
    )

    scooter_cost = hybrid_price(
    scooter_cost_raw,
    rule_scooter_cost
    )

    # Distance-based minimum pricing
    taxi_cost = max(
    taxi_cost,
    round(distance_km * 1.2, 2)
    )

    scooter_cost = max(
    scooter_cost,
    round(distance_km * 0.45, 2)
    )

    # Scooter should usually be cheaper
    if scooter_cost >= taxi_cost:
        scooter_cost = round(taxi_cost * 0.7, 2)


    # -----------------------------------------------------
    # MODE MODEL FEATURES
    # -----------------------------------------------------
    mode_features = pd.DataFrame([{
        "taxi_avg_cost": taxi_cost,
        "scooter_avg_cost": scooter_cost,
        "taxi_avg_duration": taxi_duration,
        "scooter_avg_duration": scooter_duration,
        "temperature_2m": weather["temp"],
        "relative_humidity_2m": weather["humidity"],
        "precipitation": weather["rain"],
        "windspeed_10m": weather["wind"],
        "cloudcover": weather["clouds"],
        "peak_hour": peak_hour,
    }])

    mode_features = mode_features[FEATURE_COLS]

    # -----------------------------------------------------
    # SCALE FEATURES
    # -----------------------------------------------------
    scaled = scaler.transform(mode_features)

    # -----------------------------------------------------
    # ML PREDICTION
    # -----------------------------------------------------
    prediction = best_model.predict(scaled)[0]

    probabilities = best_model.predict_proba(scaled)[0]

    confidence = round(max(probabilities) * 100, 2)

    ml_mode = "Taxi" if prediction == 0 else "Scooter"

        # =====================================================
    # PERSONALIZATION ENGINE
    # =====================================================

    if user_preference == "Cheapest":

        if scooter_cost < taxi_cost:
            ml_mode = "Scooter"
        else:
            ml_mode = "Taxi"

    elif user_preference == "Fastest":

        if taxi_duration < scooter_duration:
            ml_mode = "Taxi"
        else:
            ml_mode = "Scooter"

    elif user_preference == "Safest":

        ml_mode = "Taxi"

    # -----------------------------------------------------
    # RULE OVERRIDES
    # -----------------------------------------------------
    final_mode, reason = apply_rules(
        distance_km,
        weather,
        danger_score,
        taxi_cost,
        scooter_cost,
        ml_mode
    )

    # -----------------------------------------------------
    # EXPLAINABLE AI REASONS
    # -----------------------------------------------------

    explanations = []

    # Weather explanations
    if weather["weather"] in ["Rain", "Thunderstorm", "Snow"]:
        explanations.append(
            f"Bad weather detected ({weather['weather']})"
        )

    if weather["wind"] > 10:
        explanations.append(
            "High wind speed detected"
        )

    if danger_score > 70:
        explanations.append(
            "Danger score is very high"
        )

    # Distance explanations
    if distance_km > 15:
        explanations.append(
            "Trip distance is long"
        )

    elif distance_km < 5:
        explanations.append(
            "Trip distance is short"
        )

    # Cost explanations
    if scooter_cost < taxi_cost:
        explanations.append(
            "Scooter is cheaper"
        )

    if taxi_cost < scooter_cost:
        explanations.append(
            "Taxi pricing is competitive"
        )

    # ML explanation
    explanations.append(
        f"ML model confidence: {confidence}%"
    )

    # -----------------------------------------------------
    # RETURN RESULTS
    # -----------------------------------------------------
    return {
        "origin": origin,
        "destination": destination,

        "distance": distance_km,

        "car_time": round(taxi_duration, 2),
        "scooter_time": round(scooter_duration, 2),

        "taxi_cost": taxi_cost,
        "scooter_cost": scooter_cost,

        "final_mode": final_mode,
        "reason": reason,

        "confidence": confidence,

        "explanations": explanations,

        "danger_score": danger_score,

        "lat_o": lat_o,
        "lon_o": lon_o,
        "lat_d": lat_d,
        "lon_d": lon_d,

        "polyline": polyline,

        **weather
    }