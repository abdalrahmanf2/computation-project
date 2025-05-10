from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from model import MatchPredictor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="League of Legends Match Predictor",
             description="Predicts the outcome of a League of Legends match based on game features")

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the predictor
predictor = MatchPredictor()
try:
    predictor.load_model()
except Exception as e:
    print(f"Warning: Could not load model: {e}")

class MatchFeatures(BaseModel):
    kills: int
    total_minion_kills: int
    assist: int
    baron_kills: int
    tower_kills: int
    dragon_kills: int
    game_duration: int
    death: int

@app.post("/api/predict")
async def predict_match(features: MatchFeatures):
    """
    Predict the outcome of a League of Legends match based on game features.
    
    Returns:
        dict: Prediction results including:
            - prediction: 1 for win, 0 for loss
            - probability: Probability of winning
            - win: Boolean indicating if the team will win
    """
    try:
        print("Received features:", features)

        # Convert features to list in the correct order
        feature_values = [
            features.game_duration,
            features.dragon_kills,
            features.baron_kills,
            features.tower_kills,
            features.kills,
            features.death,
            features.assist,
            features.total_minion_kills,
        ]
        
        # Make prediction
        result = predictor.predict(feature_values)
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api")
async def root():
    """Root endpoint that returns basic API information"""
    return {
        "name": "League of Legends Match Predictor",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Predict match outcome based on game features"
        }
    } 
