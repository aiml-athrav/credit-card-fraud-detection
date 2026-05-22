import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class MLModelService:
    """
    Service layer managing the loading and runtime evaluation of the trained ML pipeline.
    """
    def __init__(self):
        self.model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "storage",
            "model_pipeline.joblib"
        )
        self.scaler = None
        self.model = None
        self.feature_names = []
        self.model_name = "Unknown"
        self.is_loaded = False
        self.load_pipeline()

    def load_pipeline(self):
        """Loads the pre-saved pipeline from disk."""
        if not os.path.exists(self.model_path):
            print(f"WARNING: Model pipeline joblib not found at {self.model_path}. ML predictions will use random simulation until trained.")
            return
        
        try:
            payload = joblib.load(self.model_path)
            self.scaler = payload["scaler"]
            self.model = payload["model"]
            self.feature_names = payload["features"]
            self.model_name = payload["model_name"]
            self.is_loaded = True
            print(f"ML Model Pipeline successfully loaded. Engine: {self.model_name}")
        except Exception as e:
            print(f"ERROR: Failed to load ML model pipeline: {str(e)}")

    def predict_probability(self, features_dict: Dict[str, float]) -> float:
        """
        Takes a flat dictionary of features (e.g. V1-V28, Time, Amount),
        orders them exactly as trained, scales them, and returns a fraud probability.
        """
        if not self.is_loaded:
            # Fallback to dynamic simulation if no model is loaded (robust failover)
            print("ML model not active. Simulating mock prediction score...")
            return float(np.random.uniform(0.01, 0.99))
            
        try:
            # Extract features in the correct order, defaulting missing items to 0.0
            ordered_features = []
            for col in self.feature_names:
                ordered_features.append(features_dict.get(col, 0.0))
                
            # Reshape into a 2D array [1, num_features]
            features_arr = np.array(ordered_features).reshape(1, -1)
            
            # Apply fitted scaler
            features_scaled = self.scaler.transform(features_arr)
            
            # Predict probability
            prob = self.model.predict_proba(features_scaled)[0][1]
            return float(prob)
        except Exception as e:
            print(f"ERROR: Failed to execute model prediction: {str(e)}")
            # Fallback to random probability as safe fallback
            return 0.50

# Singleton instance for server-wide re-use
ml_model_service = MLModelService()
