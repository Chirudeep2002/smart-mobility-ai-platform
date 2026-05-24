# apps/app.py

import os
import pandas as pd
from auth import init_users_db
import streamlit as st
import plotly.express as px
from predictor import suggest_mode
from autocomplete import get_address_suggestions
from gps import get_current_city_string
from google_map import generate_static_map
from database import init_db, save_trip
from alerts import generate_alerts


# ---------------------------------------------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Smart Ride Suggestion System (ML + Maps + Weather)",
    page_icon="🚗",
    layout="wide",
)
from auth import (
    init_users_db,
    create_user,
    validate_user,
    update_preference,
    get_preference,
    is_strong_password
)

# Initialize database
init_db()
init_users_db()

# ---------------------------------------------------------------
# GLASS UI + ANIMATIONS

st.markdown("""
<style>

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;

    background: #061126;

    color: #ffffff !important;
}

/* App Background */
.stApp {
    background:
        linear-gradient(
            135deg,
            #061126,
            #0f172a,
            #111827
        );
}
/* =========================================================
HEADINGS
========================================================= */

h1, h2, h3, h4, h5, h6 {

    color: #ffffff !important;

    font-weight: 700;
}
/* =========================================================
TEXT VISIBILITY
========================================================= */

p, li, label, span, div {

    color: #e2e8f0 !important;
}

.left-panel {

    color: white !important;
}

.left-panel h1 {

    color: white !important;

    font-size: 68px;

    font-weight: 800;

    line-height: 1.1;
}

.left-panel h2 {

    color: #cbd5e1 !important;

    font-size: 52px;

    margin-bottom: 30px;
}

.left-panel p {

    color: #cbd5e1 !important;

    font-size: 22px;

    line-height: 1.8;
}

            .login-container h1 {

    color: white !important;

    font-size: 52px;

    font-weight: 800;
}

.login-container p {

    color: #cbd5e1 !important;

    font-size: 18px;
}
.stRadio label {

    color: white !important;

    font-size: 18px;
}
.stTextInput label {

    color: #ffffff !important;

    font-size: 17px;

    font-weight: 600;
}
input::placeholder {

    color: #94a3b8 !important;
}

/* Remove Streamlit top padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================================================
LOGIN CONTAINER
========================================================= */

.login-wrapper {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 60px;

    min-height: 90vh;
}

/* =========================================================
LEFT PANEL
========================================================= */

.left-panel {

    flex: 1;

    padding: 40px;
}

.left-panel h1 {

    font-size: 64px;

    line-height: 1.1;

    font-weight: 800;

    margin-bottom: 20px;
}

.left-panel .gradient-text {

    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.left-panel p {

    font-size: 22px;

    color: #cbd5e1;

    line-height: 1.7;

    margin-bottom: 40px;
}

.feature-box {

    display: flex;

    align-items: center;

    gap: 15px;

    margin-bottom: 25px;

    background: rgba(255,255,255,0.04);

    padding: 18px;

    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.06);
}

.feature-icon {

    font-size: 28px;
}

/* =========================================================
RIGHT PANEL
========================================================= */

.right-panel {

    flex: 1;

    display: flex;

    justify-content: center;
}

/* =========================================================
LOGIN CARD
========================================================= */

.login-card {

    width: 100%;

    max-width: 520px;

    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 28px;

    padding: 45px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 8px 40px rgba(0,0,0,0.35);
}

.login-title {

    text-align: center;

    font-size: 40px;

    font-weight: 700;

    margin-bottom: 12px;
}

.login-subtitle {

    text-align: center;

    color: #cbd5e1;

    margin-bottom: 35px;
}

/* =========================================================
INPUTS
========================================================= */

/* =========================================================
TEXT INPUTS
========================================================= */

/* =========================================================
INPUT FIELDS
========================================================= */

.stTextInput input {

    background-color: #111827 !important;

    color: #ffffff !important;

    -webkit-text-fill-color: #ffffff !important;

    border: 1px solid #374151 !important;

    border-radius: 14px !important;

    padding: 14px !important;

    font-size: 18px !important;

    caret-color: #ffffff !important;
}

/* Placeholder */
.stTextInput input::placeholder {

    color: #9ca3af !important;

    opacity: 1 !important;
}

/* Password eye icon */
[data-testid="stTextInput"] svg {

    color: #d1d5db !important;
}

/* Label text */
.stTextInput label {

    color: white !important;

    font-size: 18px !important;

    font-weight: 600 !important;
}
/* =========================================================
BUTTONS
========================================================= */

.stButton>button {

    width: 100%;

    background:
        linear-gradient(
            90deg,
            #3b82f6,
            #8b5cf6
        );

    border: none;

    color: white;

    font-size: 18px;

    font-weight: 700;

    border-radius: 14px;

    padding: 14px;

    transition: 0.3s;
}

.stButton>button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(59,130,246,0.35);
}

/* =========================================================
RADIO BUTTONS
========================================================= */

.stRadio > div {

    flex-direction: row;

    gap: 30px;
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: #081224;
}
            
/* =========================================================
SELECTBOX / DROPDOWN
========================================================= */

.stSelectbox div[data-baseweb="select"] {

    background-color: #111827 !important;

    border-radius: 14px !important;

    color: white !important;
}

/* Selected value */
.stSelectbox div[data-baseweb="select"] span {

    color: white !important;
}

/* Dropdown input */
.stSelectbox input {

    color: white !important;

    -webkit-text-fill-color: white !important;
}

/* Dropdown menu */
div[role="listbox"] {

    background-color: #111827 !important;

    border: 1px solid #374151 !important;

    border-radius: 12px !important;
}

/* Dropdown items */
div[role="option"] {

    background-color: #111827 !important;

    color: white !important;

    padding: 12px !important;
}

/* Hover effect */
div[role="option"]:hover {

    background-color: #2563eb !important;

    color: white !important;
}
/* =========================================================
AUTOCOMPLETE DROPDOWN
========================================================= */

ul {

    background-color: #111827 !important;

    color: white !important;
}

/* Suggestions */
li {

    color: white !important;
}

/* Hover */
li:hover {

    background-color: #2563eb !important;

    color: white !important;
}

/* =========================================================
SELECTED SELECTBOX FIELD
========================================================= */

/* Main selectbox container */
.stSelectbox div[data-baseweb="select"] > div {

    background-color: #111827 !important;

    color: white !important;

    border: 1px solid #374151 !important;

    border-radius: 14px !important;
}

/* Selected text */
.stSelectbox div[data-baseweb="select"] div {

    color: white !important;

    -webkit-text-fill-color: white !important;
}

/* Dropdown arrow */
.stSelectbox svg {

    fill: white !important;
}

/* Placeholder text */
.stSelectbox input::placeholder {

    color: #9ca3af !important;
}

</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------------------
# AUTOCOMPLETE

def address_input(label, key):
    text = st.text_input(label, key=key)
    if len(text) >= 3:
        suggestions = get_address_suggestions(text)
        if suggestions:
            return st.selectbox("Suggestions", suggestions, key=f"{key}_s")
    return text

# ================================================================
# AUTHENTICATION
# ================================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    left, right = st.columns([1.1, 1])

    # =====================================================
    # LEFT SIDE
    # =====================================================

    with left:

        st.markdown("""
        # 🚗 Smarter Rides.
        ## Better Cities.

        AI-powered mobility recommendations for:
        - safer travel
        - faster commuting
        - intelligent ride decisions

        ---
        """)

        st.markdown("""
        ### 🧠 AI Recommendations
        Smart ML-powered ride suggestions
        """)

        st.markdown("""
        ### 🛡 Safety Intelligence
        Real-time weather and risk analysis
        """)

        st.markdown("""
        ### 📊 Smart Analytics
        Interactive mobility intelligence dashboard
        """)

    # =====================================================
    # RIGHT SIDE
    # =====================================================

    with right:

        st.markdown("""
        <div class="login-container">
            <h1>🔐 Welcome Back</h1>
            <p>Login to continue</p>
        </div>
        """, unsafe_allow_html=True)

        auth_mode = st.radio(
            "Choose Option",
            ["Login", "Signup"],
            horizontal=True
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if auth_mode == "Signup":
            st.info("""
    Password must contain:
    - 8+ characters
    - uppercase letter
    - lowercase letter
    - number
    - special character
    """)
            if st.button("Create Account"):
                if not is_strong_password(password):
                    st.error(
                """
                Weak password.

                Example:
                Chiru@123
                """
            )
                else:
                    if create_user(username, password):
                        st.success(
                    "✅ Account created successfully!"
                )
            else:
                st.error(
                    "❌ Username already exists."
                )
        else:

            if st.button("Login"):

                if validate_user(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

    st.stop()
# ================================================================
# SIDEBAR NAVIGATION
# ================================================================
st.sidebar.markdown("""
# 🚗 Smart Mobility AI

### Intelligent Ride Recommendation Platform
""")
page = st.sidebar.radio(
    "Navigation",
    ["Ride Recommendation", "Analytics Dashboard"]
)

st.sidebar.success(
    f"Logged in as: {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

# =====================================================
# USER PREFERENCE
# =====================================================

st.sidebar.markdown("---")

st.sidebar.subheader("⚙ Ride Preference")

current_pref = get_preference(
    st.session_state.username
)

preference = st.sidebar.selectbox(
    "Choose Recommendation Style",
    [
        "Balanced",
        "Cheapest",
        "Fastest",
        "Safest"
    ],
    index=[
        "Balanced",
        "Cheapest",
        "Fastest",
        "Safest"
    ].index(current_pref)
)

update_preference(
    st.session_state.username,
    preference
)

# ================================================================
# DASHBOARD PAGE
# ================================================================

if page == "Analytics Dashboard":

    from dashboard import load_trip_history

    load_trip_history()

    st.stop()
# ================================================================
# SINGLE PAGE — RIDE SUGGESTION ONLY
# ================================================================
st.markdown("""
<div class="glass-card">

# 🚗 Smart Mobility Recommendation System

### AI-Powered Taxi vs Scooter Intelligence Platform

Real-time weather • ML predictions • Route analytics • Safety scoring

</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Pickup
with col1:
    origin = address_input("Pickup Address", "origin_input")


# Drop
with col2:
    destination = address_input("Drop Address", "destination_input")

submit = st.button("🚀 Suggest Best Ride")

st.markdown("</div>", unsafe_allow_html=True)



# ================================================================
# PROCESS RESULT
# ================================================================
if submit:

    if not origin or not destination:
        st.error("❌ Please enter both pickup and destination.")
    else:
        with st.spinner("🧠 AI analyzing weather, route, cost & safety..."):
            result = suggest_mode(origin,destination,preference)
            result["username"] = st.session_state.username
            alerts = generate_alerts(result)
            result["alerts"] = alerts
        # Save trip automatically
        if "error" not in result:
            save_trip(result)

        if "error" in result:
            st.error(result["error"])

        else:
            # Save for session (critical)
            st.session_state["last_trip"] = result


            # -----------------------------------------------------------
            # MAP
            # -----------------------------------------------------------
            st.subheader("🗺 Route Map")

            map_url = generate_static_map(
            result["lat_o"],
            result["lon_o"],
            result["lat_d"],
            result["lon_d"]
            )

            st.image(
    map_url,
    use_container_width=True
)


            # -----------------------------------------------------------
            # FINAL MODE
            # -----------------------------------------------------------
            st.subheader("🚘 Final Recommendation")

            icon = "🚕" if result["final_mode"] == "Taxi" else "🛵"

            st.markdown(f"""
            <div class="result-card">
                <h2>{icon} {result['final_mode']}</h2>
                <p style="font-size:18px;">{result['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # -----------------------------------------------------------
            # AI ALERTS
            # -----------------------------------------------------------

            st.subheader("🚨 Real-Time AI Alerts")

            if alerts:

                for alert in alerts:

                    if alert["type"] == "error":
                        st.error(alert["message"])

                    elif alert["type"] == "warning":
                        st.warning(alert["message"])

                    elif alert["type"] == "success":
                        st.success(alert["message"])

                    else:
                        st.info(alert["message"])

            else:

                st.success(
                    "✅ No major alerts detected."
                )

            st.markdown("---")

            # -----------------------------------------------------------
            # CONFIDENCE SCORE
            # -----------------------------------------------------------

            st.subheader("🧠 AI Confidence")

            st.progress(result["confidence"] / 100)

            st.info(
                f"Prediction Confidence: {result['confidence']}%"
            )

            st.markdown("---")


            # -----------------------------------------------------------
            # EXPLAINABLE AI
            # -----------------------------------------------------------

            st.subheader("🤖 Why This Recommendation?")

            for item in result["explanations"]:
                st.success(f"✔ {item}")

            st.markdown("---")


            # -----------------------------------------------------------
            # COST + TIME COMPARISON
            # -----------------------------------------------------------
            st.subheader("⚖️ Taxi vs Scooter Comparison")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown(f"""
                <div class="glass-card">
                    <h3>🚕 Taxi</h3>
                    <p>⏱ Time: <b>{result['car_time']} min</b></p>
                    <p>💵 Cost: <b>${result['taxi_cost']}</b></p>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="compare-box slide-up">
                    <h3>🛵 Scooter</h3>
                    <p>⏱ Time: <b>{result['scooter_time']} min</b></p>
                    <p>💵 Cost: <b>${result['scooter_cost']}</b></p>
                </div>
                """, unsafe_allow_html=True)

            df_plot = pd.DataFrame({
                "Mode": ["Taxi", "Scooter"],
                "Cost": [result["taxi_cost"], result["scooter_cost"]],
                "Time (min)": [result["car_time"], result["scooter_time"]],
            })

            fig = px.bar(df_plot, x="Mode", y=["Cost", "Time (min)"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")


            # -----------------------------------------------------------
            # WEATHER CARD
            # -----------------------------------------------------------
            st.subheader("🌦 Weather Conditions")

            st.markdown(f"""
            <div class="glass-card">
                <p>🌤 Weather: <b>{result['weather']}</b></p>
                <p>🌡 Temp: <b>{result['temp']}°C</b></p>
                <p>💧 Humidity: <b>{result['humidity']}%</b></p>
                <p>🌬 Wind: <b>{result['wind']} m/s</b></p>
                <p>☁ Cloudiness: <b>{result['clouds']}%</b></p>
                <p>🌧 Rain: <b>{result['rain']} mm</b></p>
                <p>⚠ Danger Score: <b>{result['danger_score']}</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")


            # -----------------------------------------------------------
            # SUMMARY BAR
            # -----------------------------------------------------------
            st.markdown(f"""
            <div class="glass-card">
                <span>🚘 Mode: {result['final_mode']}</span>
                <span>📏 Distance: {result['distance']} km</span>
                <span>💵 Taxi: ${result['taxi_cost']}</span>
                <span>🛵 Scooter: ${result['scooter_cost']}</span>
                <span>⚠ Danger: {result['danger_score']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")


