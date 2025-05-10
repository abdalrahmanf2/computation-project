import joblib
import numpy as np

class MatchPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'kills', 'total_minion_kills', 'assist', 'baron_kills',
            'tower_kills', 'dragon_kills', 'game_duration', 'death'
        ]

    def load_model(self, model_path='./lol_match_predictor.joblib'):
        """Load the trained model from disk"""
        self.model = joblib.load(model_path)

    def predict(self, features):
        """Make a prediction using the loaded model"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Convert input features to numpy array and reshape for scaling
        X = np.array([features]).reshape(1, -1)
        
        # Make prediction
        prediction = self.model.predict(X)
        probability = self.model.predict_proba(X)
        
        return {
            "prediction": int(prediction[0]),
            "probability": float(probability[0][1]),
            "win": bool(prediction[0])
        } 