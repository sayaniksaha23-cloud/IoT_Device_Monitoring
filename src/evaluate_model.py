import os
import matplotlib.pyplot as plt

# Create plots directory if it doesn't exist
os.makedirs("plots", exist_ok=True)


def anomaly_summary(df):
    """
    Print overall anomaly statistics.
    """

    print("\n========== MODEL SUMMARY ==========\n")

    print(df["status"].value_counts())

    total = len(df)

    anomalies = (df["status"] == "Anomaly").sum()

    percentage = anomalies / total * 100

    print(f"\nTotal Readings : {total:,}")
    print(f"Anomalies      : {anomalies:,}")
    print(f"Percentage     : {percentage:.2f}%")
def sensor_statistics(df):
    """
    Calculate anomaly statistics for each sensor.
    """

    sensor_stats = (
        df.groupby("moteid")["status"]
        .value_counts()
        .unstack(fill_value=0)
    )

    sensor_stats["Anomaly_Percent"] = (
        sensor_stats["Anomaly"]
        /
        (
            sensor_stats["Anomaly"] +
            sensor_stats["Normal"]
        )
    ) * 100

    sensor_stats = sensor_stats.sort_values(
        by="Anomaly_Percent",
        ascending=False
    )

    print("\n========== SENSOR STATISTICS ==========\n")

    print(sensor_stats)

    return sensor_stats
def plot_anomaly_count(sensor_stats):

    plt.figure(figsize=(14,6))

    plt.bar(
        sensor_stats.index.astype(str),
        sensor_stats["Anomaly"]
    )

    plt.title("Anomalies per Sensor")

    plt.xlabel("Sensor ID")

    plt.ylabel("Number of Anomalies")

    plt.xticks(rotation=90)

    plt.tight_layout()

    plt.savefig(
        "plots/anomalies_per_sensor.png",
        dpi=300
    )

    plt.close()
def plot_anomaly_percentage(sensor_stats):

    plt.figure(figsize=(14,6))

    plt.bar(
        sensor_stats.index.astype(str),
        sensor_stats["Anomaly_Percent"]
    )

    plt.title("Anomaly Percentage per Sensor")

    plt.xlabel("Sensor ID")

    plt.ylabel("Percentage")

    plt.xticks(rotation=90)

    plt.tight_layout()

    plt.savefig(
        "plots/anomaly_percentage_per_sensor.png",
        dpi=300
    )

    plt.close()
def save_report(sensor_stats):

    sensor_stats.to_csv(
        "data/processed/sensor_statistics.csv"
    )

    print(
        "\nSensor statistics saved."
    )