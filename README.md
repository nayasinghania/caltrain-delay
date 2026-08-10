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


### CURL Request for Server Testing

- If you want to test this from the frontend, just enter the values below into the UI instead of into a curl request

```bash
curl http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id":<vehicle_id>, "station_name":<station_name>}'
```
*Go to the Caltrain website and find a vehicle id (route name) and a station name whose stop is coming soon, and put that into the request*
