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
curl http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id":137, "station_name":"San Jose Diridon"}'
```

- direction_id 0 is northbound, 1 is southbound
- vehicle id will be provided by the user
