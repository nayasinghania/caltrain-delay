from pydantic import BaseModel


class TrainData(BaseModel):
    temperature: float
    precipitation_probability: float
    precipitation: float
    wind_speed: float
    wind_gusts: float
    wind_direction: float
    visibility: float
    weather_code: int
    vehicle_id: int
    stop_sequence: int
    route_id: int
    direction_id: int
    from_stop_id: int
    to_stop_id: int
    hour: int
    minute: int
    day: int
    month: int
