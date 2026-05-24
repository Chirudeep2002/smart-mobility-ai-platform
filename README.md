# 🚖 Smart Mobility AI Platform 🛵

An AI-powered Smart Mobility Intelligence Platform that recommends the best transportation mode (Taxi or Scooter) using Machine Learning, weather intelligence, route analytics, and hybrid pricing.

🌐 **Live Demo:**  
https://mobilityai.streamlit.app/

---

# 📌 Project Overview

This platform helps users make smarter urban mobility decisions by analyzing:

- 📍 Route distance & duration
- 🌦 Real-time weather conditions
- 🚦 Traffic-aware travel estimations
- 🧠 Machine Learning ride recommendations
- 💰 Hybrid AI + rule-based pricing
- ⚠ Intelligent safety alerts
- 📊 Trip analytics dashboard
- 🔐 Secure authentication system

The system predicts whether a **Taxi** or **Scooter** is the better transportation choice based on contextual travel intelligence.

---

# 🚀 Features

## 🤖 AI-Powered Recommendation Engine
- XGBoost-based recommendation model
- Intelligent Taxi vs Scooter prediction
- Confidence score visualization

## 🌦 Weather Intelligence
- Real-time weather integration
- Rain/thunderstorm risk analysis
- Safety-aware recommendations

## 💰 Hybrid Pricing Engine
- ML-based fare prediction
- Rule-based realistic fare calibration
- Dynamic surge adjustments

## 🗺 Route Intelligence
- Google Maps integration
- Distance & ETA analysis
- Static route visualization

## 📊 Analytics Dashboard
- Trip history tracking
- Transportation insights
- User travel analytics

## 🔐 Authentication System
- Secure Login & Signup
- Password hashing with bcrypt
- SQLite-based user management

## 🎨 Modern UI/UX
- Dark SaaS-inspired interface
- Responsive design
- Interactive visualizations

---

# 🛠 Tech Stack

| Category | Technologies |
|---|---|
| Frontend | Streamlit |
| Machine Learning | XGBoost, Scikit-learn |
| Backend | Python |
| Database | SQLite |
| APIs | Google Maps API, OpenWeather API |
| Visualization | Plotly |
| Authentication | bcrypt |
| Deployment | Streamlit Cloud |

---

# 🧠 Machine Learning Architecture

The project uses a **Hybrid AI Architecture**:

### ✅ ML-Based Components
- Ride recommendation engine
- Confidence scoring
- Intelligent mobility prediction

### ✅ Rule-Based Components
- Dynamic pricing calibration
- Safety alert generation
- Weather-aware constraints

### ✅ Hybrid Fusion System
Combines:
- ML predictions
- Rule-based logic
- Realistic fare estimation

This improves:
- reliability
- explainability
- real-world practicality

---

# 📂 Project Structure

```bash
BIG DATA PROJECT/
│
├── apps/
│   ├── app.py
│   ├── predictor.py
│   ├── dashboard.py
│   ├── auth.py
│   ├── database.py
│   ├── google_map.py
│   ├── autocomplete.py
│   ├── alerts.py
│   ├── utils.py
│   ├── gps.py
│   ├── keys.py
│   ├── best_xgboost_model.pkl
│   ├── taxi_cost_model.pkl
│   ├── scooter_cost_model.pkl
│   ├── scaler.pkl
│   └── feature_cols.json
│
├── data/
│   └── trips_with_weather_best_mode_cleaned.csv
│
├── requirements.txt
└── README.md
```

---

# ⚙ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-mobility-ai-platform.git
cd smart-mobility-ai-platform
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure API Keys

Create:

```bash
.streamlit/secrets.toml
```

Add:

```toml
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
```

---

## 5️⃣ Run Application

```bash
streamlit run apps/app.py
```

---

# 🌍 Deployment

The project is deployed on Streamlit Cloud.

🔗 Live App:  
https://mobilityai.streamlit.app/

---

# 📈 Future Improvements

- 🚦 Real-time traffic integration
- 📱 Mobile optimization
- ☁ PostgreSQL cloud database
- 🐳 Docker deployment
- ⚡ FastAPI backend
- 📊 Advanced analytics
- 🧠 Deep Learning recommendation models

---

# 👨‍💻 Author

### Bandapalli Chirudeep

Master’s Student | AI & Data Engineering Enthusiast

---

# ⭐ Acknowledgements

- Google Maps Platform
- Streamlit
- Scikit-learn
- XGBoost
- Plotly

---

# 📜 License

This project is developed for academic and portfolio purposes.
