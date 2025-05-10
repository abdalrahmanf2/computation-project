# League of Legends Match Predictor API

This API predicts the outcome of a League of Legends match based on various game features.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure you have the trained model file (`model.joblib`) in the same directory as the server files.

## Running the Server

Start the server with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Making Predictions

Send a POST request to `/predict` with the following JSON structure:

```json
{
  "first_blood": 1,
  "first_tower": 1,
  "first_baron": 0,
  "first_dragon": 1,
  "first_inhibitor": 0,
  "dragon_kills": 2,
  "baron_kills": 1,
  "tower_kills": 8,
  "inhibitor_kills": 1,
  "ward_placed": 25,
  "wardkills": 10,
  "kills": 15,
  "death": 8,
  "assist": 35,
  "champion_damage_dealt": 45000,
  "total_gold": 65000,
  "total_minion_kills": 500,
  "total_level": 60,
  "avg_level": 12.0,
  "jungle_minion_kills": 120,
  "killing_spree": 5,
  "total_heal": 25000,
  "object_damage_dealt": 30000
}
```

The API will respond with:

```json
{
  "prediction": 1,
  "probability": 0.85,
  "win": true
}
```

## Features

The model uses the following features to make predictions:

- First blood, tower, baron, dragon, and inhibitor
- Number of dragon and baron kills
- Number of tower and inhibitor kills
- Ward placement and kills
- Kills, deaths, and assists
- Champion damage dealt
- Total gold
- Minion and jungle minion kills
- Team levels
- Killing sprees
- Total healing
- Object damage dealt
