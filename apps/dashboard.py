import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import os


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "trip_history.db")


# =========================================================
# LOAD DATA
# =========================================================

def load_data(username):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM trips
    WHERE username = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(username,)
    )

    conn.close()

    return df


# =========================================================
# MAIN DASHBOARD
# =========================================================

def load_trip_history():

    st.title("📊 Smart Mobility Analytics Dashboard")

    df = load_data(
    st.session_state.username
)

    # -----------------------------------------------------
    # EMPTY DATABASE
    # -----------------------------------------------------
    if df.empty:
        st.warning("No trips available yet.")
        return

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------
    st.subheader("🚀 Key Metrics")

    total_trips = len(df)

    avg_taxi_cost = round(df["taxi_cost"].mean(), 2)

    avg_scooter_cost = round(df["scooter_cost"].mean(), 2)

    avg_danger = round(df["danger_score"].mean(), 2)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Trips", total_trips)

    c2.metric("Avg Taxi Cost", f"${avg_taxi_cost}")

    c3.metric("Avg Scooter Cost", f"${avg_scooter_cost}")

    c4.metric("Avg Danger Score", avg_danger)

    st.markdown("---")

    # -----------------------------------------------------
    # MODE DISTRIBUTION
    # -----------------------------------------------------
    st.subheader("🚘 Ride Recommendation Distribution")

    fig1 = px.pie(
        df,
        names="final_mode",
        title="Taxi vs Scooter Recommendations"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -----------------------------------------------------
    # WEATHER DISTRIBUTION
    # -----------------------------------------------------
    st.subheader("🌦 Weather Conditions")

    fig2 = px.histogram(
        df,
        x="weather",
        color="final_mode",
        barmode="group"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------------------------------
    # COST COMPARISON
    # -----------------------------------------------------
    st.subheader("💵 Cost Comparison")

    cost_df = pd.DataFrame({
        "Mode": ["Taxi", "Scooter"],
        "Average Cost": [
            avg_taxi_cost,
            avg_scooter_cost
        ]
    })

    fig3 = px.bar(
        cost_df,
        x="Mode",
        y="Average Cost",
        text="Average Cost"
    )

    st.plotly_chart(fig3, use_container_width=True)


        # -----------------------------------------------------
    # COST TREND ANALYSIS
    # -----------------------------------------------------

    st.subheader("📈 Cost Trend Analysis")

    trend_df = df.copy()

    trend_df["timestamp"] = pd.to_datetime(
        trend_df["timestamp"]
    )

    trend_df = trend_df.sort_values("timestamp")

    fig_cost = px.line(
        trend_df,
        x="timestamp",
        y=["taxi_cost", "scooter_cost"],
        markers=True
    )

    st.plotly_chart(
        fig_cost,
        use_container_width=True
    )

    # -----------------------------------------------------
    # DANGER SCORE ANALYSIS
    # -----------------------------------------------------
    st.subheader("⚠ Danger Score Analysis")

    fig4 = px.scatter(
        df,
        x="distance",
        y="danger_score",
        color="final_mode",
        size="taxi_cost",
        hover_data=["weather"]
    )

    st.plotly_chart(fig4, use_container_width=True)

        # -----------------------------------------------------
    # DISTANCE DISTRIBUTION
    # -----------------------------------------------------

    st.subheader("📏 Trip Distance Distribution")

    fig_distance = px.histogram(
        df,
        x="distance",
        nbins=20,
        color="final_mode"
    )

    st.plotly_chart(
        fig_distance,
        use_container_width=True
    )

    # -----------------------------------------------------
    # TRIP TIMELINE
    # -----------------------------------------------------
    
    st.subheader("📈 Trip Timeline")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    timeline = (
        df.groupby(df["timestamp"].dt.date)
        .size()
        .reset_index(name="Trips")
    )

    fig5 = px.line(
        timeline,
        x="timestamp",
        y="Trips",
        markers=True
    )

    st.plotly_chart(fig5, use_container_width=True)

        # -----------------------------------------------------
    # PEAK HOUR ANALYSIS
    # -----------------------------------------------------

    st.subheader("⏰ Peak Hour Analysis")

    df["hour"] = df["timestamp"].dt.hour

    peak_data = (
        df.groupby("hour")
        .size()
        .reset_index(name="Trips")
    )

    fig_peak = px.bar(
        peak_data,
        x="hour",
        y="Trips",
        text="Trips"
    )

    st.plotly_chart(
        fig_peak,
        use_container_width=True
    )


        # =====================================================
    # AI SMART ANALYTICS
    # =====================================================

    st.markdown("---")

    st.subheader("🧠 AI Smart Insights")

    # -----------------------------------------------------
    # INSIGHT 1
    # -----------------------------------------------------

    most_common_weather = (
        df["weather"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"🌦 Most common travel weather condition: "
        f"{most_common_weather}"
    )

    # -----------------------------------------------------
    # INSIGHT 2
    # -----------------------------------------------------

    safest_mode = (
        df["final_mode"]
        .value_counts()
        .idxmax()
    )

    st.success(
        f"🚘 Most frequently recommended mode: "
        f"{safest_mode}"
    )

    # -----------------------------------------------------
    # INSIGHT 3
    # -----------------------------------------------------

    highest_danger_weather = (
        df.groupby("weather")["danger_score"]
        .mean()
        .idxmax()
    )

    st.warning(
        f"⚠ Highest average danger occurs during: "
        f"{highest_danger_weather}"
    )

    # -----------------------------------------------------
    # INSIGHT 4
    # -----------------------------------------------------

    cheapest_mode = (
        "Scooter"
        if avg_scooter_cost < avg_taxi_cost
        else "Taxi"
    )

    st.success(
        f"💵 Cheapest transportation overall: "
        f"{cheapest_mode}"
    )

    # -----------------------------------------------------
    # INSIGHT 5
    # -----------------------------------------------------

    avg_confidence = round(
        df["confidence"].mean(),
        2
    )

    st.info(
        f"🤖 Average AI confidence score: "
        f"{avg_confidence}%"
    )

    # -----------------------------------------------------
    # INSIGHT 6
    # -----------------------------------------------------

    high_risk_trips = len(
        df[df["danger_score"] > 70]
    )

    st.error(
        f"🚨 High-risk trips detected: "
        f"{high_risk_trips}"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # FULL DATA TABLE
    # -----------------------------------------------------
    st.subheader("📋 Trip Records")

    st.dataframe(df, use_container_width=True)