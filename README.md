# Caltrain Delay Predictor

## Setup

1. `pip install -r requirements.txt`
2. `cd app && bun install`
2. `cp .env.example .env`
3. Get a 511 API token at https://511.org/open-data/token and put into `.env`
4. Ensure you are at project root then run `python pipeline.py`

## Usage

1. `cd app/api && fastapi dev`
2. `cd app && bun dev`


*Curl request for testing*
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "precipitation_probability": 0.0,
    "visibility": 18700.0,
    "vehicle_id": 601,
    "stop_sequence": 2,
    "route_id": 3,
    "direction_id": 0,
    "from_stop_id": 70271,
    "to_stop_id": 70261,
    "hour": 9,
    "minute": 1,
    "day": 21,
    "month": 7
  }'
```
