import joblib
import openmeteo_requests
from fastapi import FastAPI
from retry_requests import retry
from schema import InputData
import pytz
from datetime import datetime
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "./xgboost.pkl"
model = joblib.load(model_path)

retry_session = retry(retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_stop_sequence(train_id, station_name):
    with open("sequences.json", "r") as f:
        data = json.load(f)

    train_id = int(train_id)

    for pattern in data["patterns"]:
        if train_id in pattern["train_ids"]:
            return pattern["stop_sequence"].get(station_name)

    return None

ROUTE_ID_MAP = {
    "1": 2,
    "4": 1,
    "5": 0,
    "6": 3,
    "8": 4,
}

def get_route_id(vehicle_id):
    first_digit = str(vehicle_id)[0]
    return ROUTE_ID_MAP.get(first_digit)

@app.post("/predict")
def predict(data: InputData):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 37.4419,
            "longitude": -122.143,
            "current": [
                "temperature_2m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "wind_speed_10m",
                "weather_code",
                "precipitation",
            ],
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        current = response.Current()
        variables = [
            "temperature_2m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "wind_speed_10m",
            "weather_code",
            "precipitation",
        ]
        current_data = {
            var: current.Variables(i).Value() for i, var in enumerate(variables)
        }

        tz = pytz.timezone("America/Los_Angeles")
        now = datetime.now(tz)
        data_dict = data.model_dump()
        features = [
            current_data["temperature_2m"],
            0.0,
            current_data["precipitation"],
            current_data["wind_speed_10m"],
            current_data["wind_gusts_10m"],
            current_data["wind_direction_10m"],
            18700.0,
            current_data["weather_code"],
            data_dict["vehicle_id"],
            get_stop_sequence(data_dict["vehicle_id"], data_dict["station_name"]),
            get_route_id(data_dict["vehicle_id"]),
            0 if data_dict['vehicle_id'] % 2 == 1 else 1,
            now.hour,
            now.minute,
            now.day,
            now.month,
        ]
        print(features)
        prediction = model.predict([features])[0]

        return {"result": float(prediction)}
    except Exception as e:
        return {"error": str(e)}
