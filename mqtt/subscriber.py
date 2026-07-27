from pathlib import Path
import sys
import json
import os

import joblib
import pandas as pd
import paho.mqtt.client as mqtt

# ---------------------------------------------------
# Add Project Root
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import *

# ---------------------------------------------------
# Load Trained Model
# ---------------------------------------------------

print("Loading trained model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")

# ---------------------------------------------------
# Features Used During Training
# ---------------------------------------------------

FEATURES = [
    "temperature",
    "humidity",
    "light",
    "voltage",
    "temp_avg_10",
    "humidity_avg_10",
    "temp_change",
    "humidity_change",
    "voltage_drop"
]

history = []

# File Paths
LATEST_FILE = PROJECT_ROOT / "latest_data.json"

LIVE_CSV = PROJECT_ROOT / "data" / "processed" / "live_predictions.csv"

# ---------------------------------------------------
# MQTT Callbacks
# ---------------------------------------------------

def on_connect(client, userdata, flags, reason_code, properties):

    print(">>> on_connect() called")
    print(f"Connected to MQTT Broker (Reason Code: {reason_code})")

    client.subscribe(MQTT_TOPIC)

    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):

    print(">>> MESSAGE RECEIVED")

    global history

    payload = json.loads(msg.payload.decode())

    history.append(payload)

    # Keep only latest 10 readings for feature engineering
    history = history[-10:]

    df = pd.DataFrame(history)

    # ---------------------------------------------------
    # Runtime Feature Engineering
    # ---------------------------------------------------

    df["temp_avg_10"] = (
        df["temperature"]
        .rolling(window=10, min_periods=1)
        .mean()
    )

    df["humidity_avg_10"] = (
        df["humidity"]
        .rolling(window=10, min_periods=1)
        .mean()
    )

    df["temp_change"] = (
        df["temperature"]
        .diff()
        .fillna(0)
    )

    df["humidity_change"] = (
        df["humidity"]
        .diff()
        .fillna(0)
    )

    df["voltage_drop"] = (
        df["voltage"]
        .diff()
        .fillna(0)
    )

    latest = df.iloc[[-1]]

    prediction = model.predict(latest[FEATURES])[0]

    status = "Normal" if prediction == 1 else "Anomaly"

    # ---------------------------------------------------
    # Output Dictionary
    # ---------------------------------------------------

    output = {

        "datetime": payload["datetime"],

        "sensor": int(payload["moteid"]),

        "temperature": float(payload["temperature"]),

        "humidity": float(payload["humidity"]),

        "light": float(payload["light"]),

        "voltage": float(payload["voltage"]),

        "status": status

    }

    # ---------------------------------------------------
    # Save Latest Reading
    # ---------------------------------------------------

    with open(LATEST_FILE, "w") as f:
        json.dump(output, f, indent=4)

    # ---------------------------------------------------
    # Append to CSV
    # ---------------------------------------------------

    row = pd.DataFrame([output])

    if LIVE_CSV.exists():

        row.to_csv(
            LIVE_CSV,
            mode="a",
            header=False,
            index=False
        )

    else:

        row.to_csv(
            LIVE_CSV,
            index=False
        )

    # ---------------------------------------------------
    # Console Output
    # ---------------------------------------------------

    print("-" * 60)

    print(f"Sensor      : {output['sensor']}")
    print(f"Temperature : {output['temperature']:.2f}")
    print(f"Humidity    : {output['humidity']:.2f}")
    print(f"Light       : {output['light']:.2f}")
    print(f"Voltage     : {output['voltage']:.2f}")
    print(f"Status      : {output['status']}")

    print("-" * 60)


# ---------------------------------------------------
# MQTT Client
# ---------------------------------------------------

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect

client.on_message = on_message

print("Connecting to MQTT Broker...")

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    keepalive=60
)
print("connect() called successfully")

print("Waiting for sensor data...")

client.loop_forever()