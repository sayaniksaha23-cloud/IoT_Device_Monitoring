import os
import matplotlib.pyplot as plt
import seaborn as sns


# Create plots directory
os.makedirs("plots", exist_ok=True)


def plot_temperature(df):
    """
    Temperature vs Time
    """

    plt.figure(figsize=(18,6))

    plt.plot(
        df["datetime"],
        df["temperature"],
        linewidth=0.5
    )

    plt.title("Temperature Over Time")
    plt.xlabel("Datetime")
    plt.ylabel("Temperature")

    plt.tight_layout()

    plt.savefig("plots/temperature_over_time.png", dpi=300)

    plt.close()


def plot_humidity(df):
    """
    Humidity vs Time
    """

    plt.figure(figsize=(18,6))

    plt.plot(
        df["datetime"],
        df["humidity"],
        linewidth=0.5
    )

    plt.title("Humidity Over Time")
    plt.xlabel("Datetime")
    plt.ylabel("Humidity")

    plt.tight_layout()

    plt.savefig("plots/humidity_over_time.png", dpi=300)

    plt.close()


def plot_histograms(df):

    features = [
        "temperature",
        "humidity",
        "light",
        "voltage"
    ]

    for feature in features:

        plt.figure(figsize=(7,4))

        plt.hist(
            df[feature],
            bins=50
        )

        plt.title(f"{feature.capitalize()} Distribution")

        plt.tight_layout()

        plt.savefig(
            f"plots/{feature}_histogram.png",
            dpi=300
        )

        plt.close()


def plot_boxplots(df):

    features = [
        "temperature",
        "humidity",
        "light",
        "voltage"
    ]

    for feature in features:

        plt.figure(figsize=(6,4))

        plt.boxplot(df[feature])

        plt.title(f"{feature.capitalize()} Boxplot")

        plt.tight_layout()

        plt.savefig(
            f"plots/{feature}_boxplot.png",
            dpi=300
        )

        plt.close()


def plot_correlation(df):

    plt.figure(figsize=(8,6))

    sns.heatmap(
        df[
            [
                "temperature",
                "humidity",
                "light",
                "voltage"
            ]
        ].corr(),
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Feature Correlation")

    plt.tight_layout()

    plt.savefig(
        "plots/correlation_heatmap.png",
        dpi=300
    )

    plt.close()


def plot_sensor1_anomalies(df):

    sensor = df[df["moteid"] == 1]

    anomalies = sensor[
        sensor["status"] == "Anomaly"
    ]

    plt.figure(figsize=(18,6))

    plt.plot(
        sensor["datetime"],
        sensor["temperature"],
        linewidth=1,
        label="Temperature"
    )

    plt.scatter(
        anomalies["datetime"],
        anomalies["temperature"],
        color="red",
        s=12,
        label="Anomaly"
    )

    plt.legend()

    plt.title("Temperature Anomalies - Sensor 1")

    plt.tight_layout()

    plt.savefig(
        "plots/temperature_anomaly_sensor1.png",
        dpi=300
    )

    plt.close()