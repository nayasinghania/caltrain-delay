import joblib
from fastapi import FastAPI
from schema import TrainData

app = FastAPI()

model_path = "./xgboost.pkl"
model = joblib.load(model_path)


@app.post("/predict")
def predict(data: TrainData):
    try:
        data_dict = data.model_dump()
        features = [
            data_dict["temperature"],
            data_dict["precipitation_probability"],
            data_dict["precipitation"],
            data_dict["wind_speed"],
            data_dict["wind_gusts"],
            data_dict["wind_direction"],
            data_dict["visibility"],
            data_dict["weather_code"],
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
