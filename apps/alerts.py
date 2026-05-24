# =========================================================
# AI ALERT ENGINE
# =========================================================

def generate_alerts(result):

    alerts = []

    # -----------------------------------------------------
    # WEATHER ALERTS
    # -----------------------------------------------------

    if result["weather"] in [
        "Thunderstorm",
        "Snow",
        "Rain"
    ]:

        alerts.append({
            "type": "error",
            "message":
            f"⚠ Severe weather detected: "
            f"{result['weather']}"
        })

    # -----------------------------------------------------
    # DANGER ALERT
    # -----------------------------------------------------

    if result["danger_score"] > 75:

        alerts.append({
            "type": "warning",
            "message":
            "🚨 High danger score detected. "
            "Travel cautiously."
        })

    # -----------------------------------------------------
    # LONG DISTANCE ALERT
    # -----------------------------------------------------

    if result["distance"] > 25:

        alerts.append({
            "type": "info",
            "message":
            "📍 Long-distance trip detected."
        })

    # -----------------------------------------------------
    # PEAK HOUR ALERT
    # -----------------------------------------------------

    if (
        result["car_time"] > 45
        and result["distance"] < 15
    ):

        alerts.append({
            "type": "warning",
            "message":
            "⏰ Heavy traffic congestion detected."
        })

    # -----------------------------------------------------
    # SURGE PRICING ALERT
    # -----------------------------------------------------

    if result["taxi_cost"] > 80:

        alerts.append({
            "type": "warning",
            "message":
            "💰 Taxi surge pricing likely active."
        })

    # -----------------------------------------------------
    # LOW CONFIDENCE ALERT
    # -----------------------------------------------------

    if result["confidence"] < 65:

        alerts.append({
            "type": "info",
            "message":
            "🤖 AI confidence is relatively low."
        })

    # -----------------------------------------------------
    # SAFE TRAVEL ALERT
    # -----------------------------------------------------

    if (
        result["danger_score"] < 30
        and result["weather"] == "Clear"
    ):

        alerts.append({
            "type": "success",
            "message":
            "✅ Weather and travel conditions are safe."
        })

    return alerts