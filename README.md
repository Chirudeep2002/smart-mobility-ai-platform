# 🚖 Smart Mobility AI Platform

> **AI-powered urban transport intelligence** — recommends the optimal travel mode (Taxi vs. Scooter) using Machine Learning, real-time weather, route analytics, and hybrid pricing.

🌐 **Live Demo:** [mobilityai.streamlit.app](https://mobilityai.streamlit.app/)
&nbsp;&nbsp;|&nbsp;&nbsp;
📁 **GitHub:** [smart-mobility-ai-platform](https://github.com/Chirudeep2002/smart-mobility-ai-platform)

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| 📦 Dataset Size | **307,788** trip records |
| 🚕 Total Rides Analyzed | **3.5M+** (2.68M taxi + 850K scooter) |
| 📅 Date Coverage | Oct 2022 – Jan 2023 |
| 🤖 Model Accuracy | **~99.9%** (XGBoost classifier) |
| 🌦 Weather Features | Temperature, Wind Speed, Precipitation, Humidity, Cloud Cover |
| 🔗 Live APIs | Google Maps API · OpenWeather API |

---

## 🧠 What It Does

This platform helps urban commuters make smarter mobility decisions by fusing real-world trip data with live weather and route intelligence. Given a user's trip context, the system predicts whether **Taxi** or **Scooter** is the optimal choice — factoring in cost, duration, weather safety, and traffic patterns.

Key finding from the data: **weather is the dominant signal** — temperature and wind speed together account for ~96% of the model's predictive power, validating the real-world intuition that weather drives transport mode choice.

---

## 🚀 Features

### 🤖 AI Recommendation Engine
- XGBoost-based binary classifier (Taxi vs. Scooter)
- Trained on 307K+ real trip records across multiple weather conditions
- Confidence score visualization per recommendation
- ~99.9% test-set accuracy

### 💰 Hybrid Pricing Engine
- ML-based fare prediction (separate models for Taxi and Scooter)
- Rule-based calibration layer for real-world fare accuracy
- Dynamic surge pricing adjustments based on peak hours and weather

### 🌦 Weather Intelligence
- Real-time OpenWeather API integration
- Rain, thunderstorm, and extreme wind safety detection
- Weather-aware safety alerts before trip confirmation

### 🗺️ Route Intelligence
- Google Maps API integration for distance and ETA
- Static route visualization
- Traffic-aware travel time estimation

### 📊 Analytics Dashboard
- Personal trip history tracking
- Mode split analytics (Taxi vs. Scooter usage)
- Cost savings tracking over time

### 🔐 Secure Authentication
- Bcrypt password hashing
- SQLite-backed user management
- Session state management

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **ML Models** | XGBoost · Scikit-learn · Pandas · NumPy |
| **Backend** | Python · SQLite · bcrypt |
| **APIs** | Google Maps Platform · OpenWeather API |
| **Frontend** | Streamlit · Custom CSS · Plotly |
| **Deployment** | Streamlit Community Cloud |
| **Model Artifacts** | `.pkl` (XGBoost, Taxi cost, Scooter cost models) |

---

## 🧠 ML Architecture

The system uses a **Hybrid AI Architecture** combining two layers:

```
User Input (route, time, location)
        │
        ▼
┌─────────────────────────────────┐
│     Weather + Route Context     │  ← OpenWeather + Google Maps APIs
└────────────────┬────────────────┘
                 │
        ┌────────▼────────┐
        │  XGBoost Model  │  ← Trained on 307K+ trips
        │  (Taxi/Scooter) │    Top features: temperature, wind
        └────────┬────────┘
                 │
        ┌────────▼────────────────────┐
        │   Hybrid Pricing Engine     │  ← ML fare + rule-based calibration
        └────────┬────────────────────┘
                 │
        ┌────────▼────────┐
        │  Recommendation │  + confidence score + safety alerts
        └─────────────────┘
```

### Feature Importance (Top 5)

| Feature | Importance |
|---|---|
| Temperature (°C) | 51.8% |
| Wind Speed (km/h) | 43.9% |
| Precipitation | 3.5% |
| Peak Hour | 0.6% |
| Cost Difference | 0.1% |

---

## 📂 Project Structure

```
smart-mobility-ai-platform/
│
├── apps/
│   ├── app.py                  # Main Streamlit entrypoint
│   ├── predictor.py            # XGBoost inference logic
│   ├── dashboard.py            # Analytics dashboard
│   ├── auth.py                 # Login / signup
│   ├── database.py             # SQLite operations
│   ├── google_map.py           # Maps API integration
│   ├── alerts.py               # Safety alert engine
│   ├── utils.py                # Shared utilities
│   ├── best_xgboost_model.pkl  # Trained classifier
│   ├── taxi_cost_model.pkl     # Taxi fare model
│   └── scooter_cost_model.pkl  # Scooter fare model
│
├── data/
│   └── trips_with_weather_best_mode_cleaned.csv
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/Chirudeep2002/smart-mobility-ai-platform.git
cd smart-mobility-ai-platform

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
# Create .streamlit/secrets.toml and add:
# GOOGLE_API_KEY = "YOUR_KEY"
# OPENWEATHER_API_KEY = "YOUR_KEY"

# 5. Run
streamlit run apps/app.py
```

---

## 🔮 Roadmap

- [ ] Real-time traffic API integration
- [ ] PostgreSQL migration for production scale
- [ ] Docker containerization
- [ ] FastAPI backend decoupling
- [ ] Deep Learning recommendation upgrade
- [ ] Mobile-responsive PWA

---

## 👨‍💻 Author

**Bandapalli Chirudeep**
MS Computer Science · UNC Charlotte · AI & Data Engineering

[![LinkedIn](https://img.shields.io/badge/LinkedIn-chirudeepbandapalli-blue?style=flat&logo=linkedin)](https://linkedin.com/in/chirudeepbandapalli)
[![GitHub](https://img.shields.io/badge/GitHub-Chirudeep2002-black?style=flat&logo=github)](https://github.com/Chirudeep2002)
[![Portfolio](https://img.shields.io/badge/Portfolio-chirudeep--portfolio.vercel.app-green?style=flat)](https://chirudeep-portfolio.vercel.app)
