import pandas as pd

fires = pd.read_csv("data/raw/cal-fire-incident.csv")

fires = fires[
    [
        "incident_date_created",
        "incident_latitude",
        "incident_longitude",
        "incident_acres_burned",
    ]
]

fires.columns = ["date", "lat", "lon", "acres"]

fires["date"] = pd.to_datetime(fires["date"]).dt.date

fires["acres"] = fires["acres"].fillna(0).astype(int)
fires["lat"] = fires["lat"].round(2)
fires["lon"] = fires["lon"].round(2)

print(fires.head())
print(fires.tail())
