"""
Downloader for monthly Open-Meteo historical weather data.

Given a period [start, end] inclusive (by month), this script downloads
`weather_YYYY-MM.json` files to a target directory (default: `data/weather`).
"""

import json
import os
from datetime import datetime

import openmeteo_requests
import requests_cache
from dateutil.relativedelta import relativedelta
from retry_requests import retry


def get_weather(openmeteo, latitude, longitude, start_date, end_date, output_dir):
    """Download monthly weather data for a given location.

    Parameters:
    - openmeteo: openmeteo_requests.Client – configured API client.
    - latitude: float – Location latitude.
    - longitude: float – Location longitude.
    - start_date: datetime – Inclusive start (only year/month used).
    - end_date: datetime – Inclusive end (only year/month used).
    - output_dir: str – Directory to save `weather_YYYY-MM.json` files.
    """
    os.makedirs(output_dir, exist_ok=True)
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    current = start_date
    while current <= end_date:
        month_start = current.strftime("%Y-%m-01")
        next_month = current + relativedelta(months=1)
        month_end = (next_month - relativedelta(days=1)).strftime("%Y-%m-%d")
        ym = current.strftime("%Y-%m")
        fname = f"weather_{ym}.json"
        path = os.path.join(output_dir, fname)
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": month_start,
            "end_date": month_end,
            "hourly": [
                "temperature_2m",
                "precipitation_probability",
                "precipitation",
                "wind_speed_10m",
                "wind_gusts_10m",
                "wind_direction_10m",
                "visibility",
                "weather_code",
            ],
        }
        print(f"Fetching: {ym}")
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        variables = [
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
            "wind_gusts_10m",
            "wind_direction_10m",
            "visibility",
            "weather_code",
        ]
        raw = {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "elevation": response.Elevation(),
            "utc_offset_seconds": response.UtcOffsetSeconds(),
            "hourly_time_start": hourly.Time(),
            "hourly_time_end": hourly.TimeEnd(),
            "hourly_interval": hourly.Interval(),
            "hourly": {
                var: hourly.Variables(i).ValuesAsNumpy().tolist()
                for i, var in enumerate(variables)
            },
        }
        with open(path, "w") as f:
            json.dump(raw, f)
        print(f"Saved {fname}")
        current = next_month


if __name__ == "__main__":
    retry_session = retry(retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    latitude = 37.4419
    longitude = -122.143
    start_date = datetime(2025, 3, 1)
    end_date = datetime(2026, 2, 28)
    output_dir = "data/weather"

    get_weather(openmeteo, latitude, longitude, start_date, end_date, output_dir)
