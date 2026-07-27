from pathlib import Path
import sys
import json
import time
import random

import pandas as pd
import paho.mqtt.client as mqtt

# ---------------------------------------------------
# Add project root
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import *

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

import os

LIVE_CSV = PROJECT_ROOT / "data" / "processed" / "live_predictions.csv"

if LIVE_CSV.exists():
    os.remove(LIVE_CSV)

LATEST_JSON = PROJECT_ROOT / "latest_data.json"

if LATEST_JSON.exists():
    os.remove(LATEST_JSON)
print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

# Remove invalid rows
df = df.dropna()

# Sort chronologically
df = df.sort_values("datetime")

# Use first 20,000 readings
df = df.head(20000)

print(f"Loaded {len(df)} readings.")

# ---------------------------------------------------
# MQTT Callbacks
# ---------------------------------------------------

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    keepalive=60
)

client.loop_start()

time.sleep(2)

print("\nPublishing sensor data...\n")

# ---------------------------------------------------
# Publish Forever
# ---------------------------------------------------
for _, row in df.iterrows():

        payload = {

            "datetime": str(row["datetime"]),

            "moteid": int(row["moteid"]),

            "temperature": float(row["temperature"]),

            "humidity": float(row["humidity"]),

            "light": float(row["light"]),

            "voltage": float(row["voltage"])

        }

        # ------------------------------------------
        # Simulate Sensor Faults (2% probability)
        # ------------------------------------------

        if random.random() < 0.02:

            anomaly = random.choice([
                "temperature",
                "humidity",
                "light",
                "voltage"
            ])

            if anomaly == "temperature":
                payload["temperature"] += random.uniform(20,40)

            elif anomaly == "humidity":
                payload["humidity"] = random.uniform(-30,150)

            elif anomaly == "light":
                payload["light"] *= random.uniform(2.5,5)

            elif anomaly == "voltage":
                payload["voltage"] *= random.uniform(0.3,0.7)

        client.publish(
            MQTT_TOPIC,
            json.dumps(payload),
            qos=1
        )

        print(payload)

        time.sleep(PUBLISH_DELAY)