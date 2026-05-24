# apps/utils.py

import requests
from keys import OPENWEATHER_API_KEY


def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url).json()

        weather = r["weather"][0]["main"]
        temp = r["main"]["temp"]
        humidity = r["main"]["humidity"]
        wind = r["wind"]["speed"]
        clouds = r["clouds"]["all"]
        rain = r.get("rain", {}).get("1h", 0)

        eco_score = round((clouds + humidity) * 0.2, 2)

        return {
            "weather": weather,
            "temp": temp,
            "humidity": humidity,
            "wind": wind,
            "clouds": clouds,
            "rain": rain,
            "eco_score": eco_score,
        }
    except:
        return {
            "weather": "Clear",
            "temp": 20,
            "humidity": 50,
            "wind": 3,
            "clouds": 10,
            "rain": 0,
            "eco_score": 5,
        }


def compute_danger_score(w):
    score = 0
    score += (w["humidity"] / 100) * 25
    score += (w["wind"] / 20) * 25
    score += (w["clouds"] / 100) * 20
    if w["weather"] in ["Rain", "Thunderstorm", "Snow"]:
        score += 30

    return round(min(score, 100), 2)


def apply_rules(distance_km, weather, danger_score, taxi_cost, scooter_cost, ml_mode):

    # Hard safety override
    if weather["weather"] in ["Rain", "Snow", "Thunderstorm"]:
        return "Taxi", "Unsafe weather detected — Taxi is safer."

    # High danger score
    if danger_score > 70:
        return "Taxi", "Danger score too high for scooter."

    # Long distance override > 10 miles (16 km)
    if distance_km > 16:
        return "Taxi", "Distance too long for scooter."

    # Very short trips (<5 miles / 8km)
    if distance_km < 8:
        if scooter_cost < taxi_cost:
            return "Scooter", "Short trip — scooter is cheapest."
        else:
            return "Taxi", "Short trip — taxi cost reasonable."

    # Otherwise trust ML
    return ml_mode, "AI-based recommendation under normal conditions."
