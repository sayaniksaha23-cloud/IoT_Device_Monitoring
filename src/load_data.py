import pandas as pd
from pathlib import Path


# Column names for the Intel Berkeley dataset
COLUMNS = [
    "date",
    "time",
    "epoch",
    "moteid",
    "temperature",
    "humidity",
    "light",
    "voltage"
]


def load_dataset(file_path=None):
    """
    Load the Intel Berkeley sensor dataset.

    Parameters
    ----------
    file_path : str or Path, optional
        Path to the raw sensor data file.
        If not provided, the default location is used.

    Returns
    -------
    pandas.DataFrame
        Loaded sensor dataset.
    """

    if file_path is None:
        project_root = Path(__file__).resolve().parent.parent
        file_path = project_root / "data" / "raw" / "sensor_data.txt"

    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        names=COLUMNS,
        on_bad_lines="skip"
    )

    # Keep only valid sensor IDs
    df = df[
        (df["moteid"] >= 1) &
        (df["moteid"] <= 54)
    ]

    print(f"Dataset loaded successfully.")
    print(f"Total records: {len(df):,}")

    return df