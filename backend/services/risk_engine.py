import numpy as np
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from schemas.transaction import TransactionCreate
from models.transaction import Transaction
from repositories import transaction_repository, prediction_repository
from services.ml_model import ml_model_service

class RiskEngineService:
    """
    Core business rule processor combining machine learning scoring with corporate risk policy logic.
    """
    
    def generate_simulated_features(self, profile: str, amount: float) -> Dict[str, float]:
        """
        Creates a V1-V28 PCA feature set matching genuine, suspicious,
        or fraudulent distributions. Ensures realistic simulation testing.
        """
        features = {}
        # Simulate Time as standard seconds elapsed
        features["Time"] = float(np.random.uniform(0, 172800))
        features["Amount"] = float(amount)
        
        # Populate default standard normal features
        for i in range(1, 29):
            features[f"V{i}"] = float(np.random.normal(0.0, 1.0))
            
        # Introduce shifted means depending on testing profiles
        if profile == "suspicious":
            # Shift discriminative features moderately
            features["V3"] = float(np.random.normal(-1.2, 1.0))
            features["V4"] = float(np.random.normal(1.5, 1.0))
            features["V11"] = float(np.random.normal(1.2, 1.0))
            features["V12"] = float(np.random.normal(-1.5, 1.0))
            features["V14"] = float(np.random.normal(-2.0, 1.0))
            features["V17"] = float(np.random.normal(-2.2, 1.0))
        elif profile == "fraudulent":
            # Shift discriminative features aggressively to guarantee block
            features["V3"] = float(np.random.normal(-3.5, 1.0))
            features["V4"] = float(np.random.normal(4.0, 1.0))
            features["V10"] = float(np.random.normal(-3.0, 1.0))
            features["V11"] = float(np.random.normal(3.5, 1.0))
            features["V12"] = float(np.random.normal(-4.5, 1.0))
            features["V14"] = float(np.random.normal(-5.5, 1.0))
            features["V16"] = float(np.random.normal(-3.5, 1.0))
            features["V17"] = float(np.random.normal(-6.0, 1.0))
            
        return features

    def process_transaction(
        self, db: Session, transaction_in: TransactionCreate, user_id: Optional[int] = None
    ) -> Transaction:
        """
        Orchestrates full prediction evaluation pipeline:
        1. Prepares features (either provided explicitly or auto-simulated from profiles).
        2. Evaluates model probability.
        3. Folds probability into thresholds to assign status.
        4. Saves Transaction & Prediction logs atomically.
        """
        # 1. Prepare feature dictionary
        if transaction_in.features:
            features = transaction_in.features
            # Ensure Amount and Time are included in features dictionary
            if "Amount" not in features:
                features["Amount"] = float(transaction_in.amount)
            if "Time" not in features:
                features["Time"] = float(np.random.uniform(0, 172800))
        else:
            features = self.generate_simulated_features(
                transaction_in.profile or "genuine",
                transaction_in.amount
            )
            
        # 2. Extract ML Probability
        probability = ml_model_service.predict_probability(features)
        
        # 3. Categorize Risk Thresholds
        if probability < 0.30:
            status = "APPROVED"
        elif 0.30 <= probability < 0.70:
            status = "REVIEW"
        else:
            status = "BLOCKED"
            
        # 4. Save transaction
        db_transaction = transaction_repository.create_transaction(
            db=db,
            amount=transaction_in.amount,
            card_number=transaction_in.card_number,
            merchant=transaction_in.merchant,
            status=status,
            user_id=user_id
        )
        
        # 5. Save prediction audit record linked to transaction
        prediction_repository.create_prediction(
            db=db,
            transaction_id=db_transaction.id,
            probability=probability,
            decision=status,
            features=features,
            model_version="1.0.0"
        )
        
        # Refresh and return
        db.refresh(db_transaction)
        return db_transaction

risk_engine_service = RiskEngineService()
