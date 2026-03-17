import csv
import json
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta, timezone

start_year = 2025
end_year = 2026
start_month = 3
end_month = 2

HOURLY_FIELDS = [
    "temperature_2m: temperature",
    "precipitation_probability",
    "precipitation",
    "wind_speed_10m: wind_speed",
    "wind_gusts_10m: wind_gusts",
    "wind_direction_10m: wind_direction",
    "visibility",
    "weather_code",
]


# Parse "json_key: csv_name" or plain "field" entries
def _parse_field(f):
    if ": " in f:
        json_key, csv_name = f.split(": ", 1)
        return json_key.strip(), csv_name.strip()
    return f, f


HOURLY_FIELD_PAIRS = [_parse_field(f) for f in HOURLY_FIELDS]
CSV_COLUMNS = [csv_name for _, csv_name in HOURLY_FIELD_PAIRS]


def weather_csv():
    with open("./data/weather.csv", "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["timestamp"] + CSV_COLUMNS)
        writer.writeheader()
        for y in range(start_year, end_year + 1):
            m_start = start_month if y == start_year else 1
            m_end = end_month if y == end_year else 12
            for m in range(m_start, m_end + 1):
                try:
                    with open(f"./data/weather/weather_{y}-{m:02d}.json") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    continue
                t = datetime.fromtimestamp(data["hourly_time_start"], tz=timezone.utc)
                interval = timedelta(seconds=data["hourly_interval"])
                hourly = data["hourly"]
                first_json_key = HOURLY_FIELD_PAIRS[0][0]
                n = len(hourly[first_json_key])
                for i in range(n):
                    hour_t = t + i * interval
                    values = {}
                    for json_key, csv_name in HOURLY_FIELD_PAIRS:
                        v = hourly[json_key][i]
                        values[csv_name] = "" if v != v else "{:.3f}".format(v)
                    for minute in range(60):
                        row = {
                            "timestamp": (hour_t + timedelta(minutes=minute)).strftime(
                                "%Y-%m-%dT%H:%M"
                            )
                        }
                        row.update(values)
                        writer.writerow(row)


STOP_OBS_KEEP = [
    "trip_id",
    "vehicle_id",
    "stop_sequence",
    "observed_arrival_time",
    "observed_departure_time",
    "scheduled_arrival_time",
    "scheduled_departure_time",
    "dwell_time_secs",
    "route_id",
    "direction_id",
    "from_stop_id",
    "to_stop_id",
]


def _parse_gtfs_time(service_date, time_str):
    """Parse GTFS service_date (YYYYMMDD) + time (HH:MM:SS, HH may be >= 24)."""
    date = datetime.strptime(service_date, "%Y%m%d")
    h, m, s = map(int, time_str.split(":"))
    return date + timedelta(hours=h, minutes=m, seconds=s)


_weather = {}


def _init_worker(w):
    global _weather
    _weather = w


def _process_month(args):
    y, m = args
    path = f"./data/gtfs_unzipped/{y}-{m:02d}/stop_observations.txt"
    rows = []
    try:
        f = open(path, newline="")
    except FileNotFoundError:
        return rows
    with f:
        print(f"processing {path}")
        for obs in csv.DictReader(f):
            if obs["agency_id"] != "CT":
                continue
            if not obs["observed_arrival_time"]:
                continue
            dt = _parse_gtfs_time(obs["service_date"], obs["observed_arrival_time"])
            ts = dt.strftime("%Y-%m-%dT%H:%M")
            w = _weather.get(ts, {})
            row = {"timestamp": ts}
            row.update({k: w.get(k, "") for k in CSV_COLUMNS})
            row.update({k: obs[k] for k in STOP_OBS_KEEP})
            rows.append(row)
    print(f"done {path}: {len(rows)} rows")
    return rows


def gtfs_csv():
    weather = {}
    with open("./data/weather.csv", newline="") as f:
        for row in csv.DictReader(f):
            weather[row["timestamp"]] = row

    months = []
    for y in range(start_year, end_year + 1):
        m_start = start_month if y == start_year else 1
        m_end = end_month if y == end_year else 12
        for m in range(m_start, m_end + 1):
            months.append((y, m))

    with open("./data.csv", "w", newline="") as out:
        fieldnames = ["timestamp"] + CSV_COLUMNS + STOP_OBS_KEEP
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        with ProcessPoolExecutor(
            max_workers=os.cpu_count(),
            initializer=_init_worker,
            initargs=(weather,),
        ) as ex:
            for rows in ex.map(_process_month, months):
                for row in rows:
                    writer.writerow(row)


if __name__ == "__main__":
    weather_csv()
    gtfs_csv()
