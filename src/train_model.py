import os
import joblib
from sklearn.ensemble import IsolationForest


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


def train_model(df):
    """
    Train Isolation Forest and predict anomalies.
    """

    print("Training Isolation Forest model...")

    X = df[FEATURES]

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    model.fit(X)

    predictions = model.predict(X)

    df["prediction"] = predictions

    df["status"] = df["prediction"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    print("Model training completed.")

    return model, df


def save_model(model):
    """
    Save trained model.
    """

    os.makedirs("models", exist_ok=True)

    model_path = "models/anomaly_model.pkl"

    joblib.dump(model, model_path)

    print(f"Model saved to {model_path}")


def save_predictions(df):
    """
    Save predictions.
    """

    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/predicted_sensor_data.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Predictions saved to {output_path}")