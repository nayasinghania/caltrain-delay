from pydantic import BaseModel


class TrainData(BaseModel):
    vehicle_id: int
    stop_sequence: int
    route_id: int

class InputData(BaseModel):
    vehicle_id: int
    station_name: str
