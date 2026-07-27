from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "data" / "processed" / "live_predictions.csv"

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI IoT Monitoring Platform",
    page_icon="📡",
    layout="wide"
)

# Refresh every second
st_autorefresh(interval=1000, key="refresh")

st.title("📡 AI Powered IoT Device Monitoring Platform")

# -----------------------------
# Load Data
# -----------------------------

if not CSV_FILE.exists():

    st.warning("Waiting for sensor data...")
    st.stop()

df = pd.read_csv(CSV_FILE)

if len(df) == 0:

    st.warning("No sensor data available.")
    st.stop()
st.sidebar.title("Dashboard Controls")

sensor_list = ["All"] + sorted(df["sensor"].unique().tolist())

selected_sensor = st.sidebar.selectbox(
    "Select Sensor",
    sensor_list
)

if selected_sensor != "All":

    df = df[df["sensor"] == selected_sensor]
latest = df.iloc[-1]

total = len(df)

anomalies = len(df[df["status"] == "Anomaly"])

normal = total - anomalies

percent = anomalies / total * 100
c1, c2, c3, c4 = st.columns(4)

c1.metric("Messages", total)

c2.metric("Normal", normal)

c3.metric("Anomalies", anomalies)

c4.metric("Anomaly %", f"{percent:.2f}%")
st.divider()

st.subheader("Current Sensor")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperature",
    f"{latest['temperature']:.2f} °C"
)

col2.metric(
    "Humidity",
    f"{latest['humidity']:.2f} %"
)

col3.metric(
    "Light",
    f"{latest['light']:.2f}"
)

col4.metric(
    "Voltage",
    f"{latest['voltage']:.2f} V"
)
if latest["status"] == "Normal":

    st.success("🟢 Device Operating Normally")

else:

    st.error("🔴 Anomaly Detected")
    st.divider()

st.subheader("🌡 Temperature Trend")

st.line_chart(
    df.set_index("datetime")["temperature"]
)
st.subheader("💧 Humidity Trend")

st.line_chart(
    df.set_index("datetime")["humidity"]
)
st.subheader("💡 Light Trend")

st.line_chart(
    df.set_index("datetime")["light"]
)
st.subheader("🔋 Voltage Trend")

st.line_chart(
    df.set_index("datetime")["voltage"]
)
st.divider()

st.subheader("Latest Sensor Readings")

st.dataframe(
    df.tail(20),
    use_container_width=True
)
st.divider()

st.subheader("Anomalies Per Sensor")

anomaly_counts = (
    df[df["status"] == "Anomaly"]
    .groupby("sensor")
    .size()
)

st.bar_chart(anomaly_counts)