from pydantic import BaseModel


class TrainData(BaseModel):
    precipitation_probability: float
    visibility: float
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
