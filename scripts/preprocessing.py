import pandas as pd
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

print("\nLoading data/data-full.csv")
df = pd.read_csv("./data/data-full.csv")
print("Loaded data/data-full.csv")
print("Preprocessing Data")

df = df.dropna()

df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M")
df.sort_values(by=["timestamp"], inplace=True)
df.reset_index(drop=True, inplace=True)

df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month

df["observed_arrival_time"] = pd.to_timedelta(df["observed_arrival_time"])  # type: ignore
df["scheduled_arrival_time"] = pd.to_timedelta(df["scheduled_arrival_time"])  # type: ignore
df["delay"] = (
    df["observed_arrival_time"] - df["scheduled_arrival_time"]
).dt.total_seconds() / 60

df["route_id"] = label_encoder.fit_transform(df["route_id"])

df = df.drop(
    columns=[
        "timestamp",
        "trip_id",
        "dwell_time_secs",
        "scheduled_departure_time",
        "observed_departure_time",
        "observed_arrival_time",
        "scheduled_arrival_time",
    ]
)

df["delay"] = df["delay"].round(3)

print("Exporting preprocessed data to data-preproc.csv")
df.to_csv("data/data.csv", index=False)
print("Exported preprocessed data to data-preproc.csv")
