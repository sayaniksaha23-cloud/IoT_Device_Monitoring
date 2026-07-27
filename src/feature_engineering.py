import os
import pandas as pd


def create_features(df):
    """
    Create machine learning features from the cleaned sensor dataset.

    Features:
    1. Rolling average temperature
    2. Rolling average humidity
    3. Temperature change
    4. Humidity change
    5. Voltage change
    """

    print("Creating features...")

    # Rolling average temperature
    df["temp_avg_10"] = (
        df.groupby("moteid")["temperature"]
        .transform(
            lambda x: x.rolling(
                window=10,
                min_periods=1
            ).mean()
        )
    )

    # Rolling average humidity
    df["humidity_avg_10"] = (
        df.groupby("moteid")["humidity"]
        .transform(
            lambda x: x.rolling(
                window=10,
                min_periods=1
            ).mean()
        )
    )

    # Temperature difference
    df["temp_change"] = (
        df.groupby("moteid")["temperature"]
        .diff()
        .fillna(0)
    )

    # Humidity difference
    df["humidity_change"] = (
        df.groupby("moteid")["humidity"]
        .diff()
        .fillna(0)
    )

    # Voltage difference
    df["voltage_drop"] = (
        df.groupby("moteid")["voltage"]
        .diff()
        .fillna(0)
    )

    print("Feature engineering completed.")

    return df


def save_engineered_data(df):
    """
    Save engineered dataset.
    """

    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/engineered_sensor_data.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Engineered dataset saved to {output_path}")