import sqlite3
import os
from datetime import datetime


# ======================================================
# DATABASE PATH
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "trip_history.db")


# ======================================================
# CREATE TABLE
# ======================================================

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        timestamp TEXT,
        username TEXT,
        origin TEXT,
        destination TEXT,

        distance REAL,

        weather TEXT,
        temperature REAL,
        humidity REAL,
        wind REAL,
        clouds REAL,
        rain REAL,

        taxi_cost REAL,
        scooter_cost REAL,

        taxi_time REAL,
        scooter_time REAL,

        danger_score REAL,

        final_mode TEXT,

        confidence REAL,
        alerts TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================================
# SAVE TRIP
# ======================================================

def save_trip(result):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trips (

    timestamp,

    username,

    origin,
    destination,

    distance,

    weather,
    temperature,
    humidity,
    wind,
    clouds,
    rain,

    taxi_cost,
    scooter_cost,

    taxi_time,
    scooter_time,

    danger_score,

    final_mode,

    confidence,

    alerts
)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    result["username"],

    result["origin"],
    result["destination"],

    result["distance"],

    result["weather"],
    result["temp"],
    result["humidity"],
    result["wind"],
    result["clouds"],
    result["rain"],

    result["taxi_cost"],
    result["scooter_cost"],

    result["car_time"],
    result["scooter_time"],

    result["danger_score"],

    result["final_mode"],

    float(result["confidence"]),

    str(result.get("alerts", []))
    ))

    conn.commit()
    conn.close()