import os
import pandas as pd


def preprocess_data(df):
    """
    Clean the sensor dataset.

    Steps:
    1. Combine date and time
    2. Convert to datetime
    3. Remove invalid datetime values
    4. Remove duplicate rows
    5. Sort data by sensor and time

    Returns
    -------
    pandas.DataFrame
    """

    print("Starting preprocessing...")

    # Combine date and time
    df["datetime"] = pd.to_datetime(
        df["date"].astype(str) + " " + df["time"].astype(str),
        errors="coerce"
    )

    # Remove invalid datetime rows
    df = df.dropna(subset=["datetime"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Sort by sensor and timestamp
    df = df.sort_values(
        by=["moteid", "datetime"]
    ).reset_index(drop=True)

    print(f"Rows after preprocessing: {len(df):,}")

    return df


def save_clean_data(df):
    """
    Save cleaned dataset.
    """

    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/cleaned_sensor_data.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Cleaned dataset saved to {output_path}")