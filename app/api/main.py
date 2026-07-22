import joblib
import openmeteo_requests
from fastapi import FastAPI
from retry_requests import retry
from schema import TrainData

app = FastAPI()

model_path = "./xgboost.pkl"
model = joblib.load(model_path)

retry_session = retry(retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


@app.post("/predict")
def predict(data: TrainData):
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
        print(current_data)
        data_dict = data.model_dump()
        features = [
            current_data["temperature_2m"],
            data_dict["precipitation_probability"],
            current_data["precipitation"],
            current_data["wind_speed_10m"],
            current_data["wind_gusts_10m"],
            current_data["wind_direction_10m"],
            data_dict["visibility"],
            current_data["weather_code"],
            data_dict["vehicle_id"],
            data_dict["stop_sequence"],
            data_dict["route_id"],
            data_dict["direction_id"],
            data_dict["from_stop_id"],
            data_dict["to_stop_id"],
            data_dict["hour"],
            data_dict["minute"],
            data_dict["day"],
            data_dict["month"],
        ]
        prediction = model.predict([features])[0]

        return {"result": float(prediction)}
    except Exception as e:
        return {"error": str(e)}
