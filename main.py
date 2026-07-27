from src.load_data import load_dataset
from src.preprocess import preprocess_data, save_clean_data
from src.feature_engineering import (
    create_features,
    save_engineered_data
)
from src.train_model import (
    train_model,
    save_model,
    save_predictions
)
from src.visualization import (
    plot_temperature,
    plot_humidity,
    plot_histograms,
    plot_boxplots,
    plot_correlation,
    plot_sensor1_anomalies
)
from src.evaluate_model import (
    anomaly_summary,
    sensor_statistics,
    plot_anomaly_count,
    plot_anomaly_percentage,
    save_report
)

# Load data
df = load_dataset()

# Preprocess
df = preprocess_data(df)
save_clean_data(df)

# Feature Engineering
df = create_features(df)
save_engineered_data(df)

# Train Model
model, df = train_model(df)

# Save Model
save_model(model)

# Save Predictions
save_predictions(df)

print(df.head())
print("Generating plots...")

plot_temperature(df)
plot_humidity(df)
plot_histograms(df)
plot_boxplots(df)
plot_correlation(df)
plot_sensor1_anomalies(df)

print("Plots saved successfully.")
print("Evaluating model...")

anomaly_summary(df)

sensor_stats = sensor_statistics(df)

plot_anomaly_count(sensor_stats)

plot_anomaly_percentage(sensor_stats)

save_report(sensor_stats)

print("Evaluation completed.")