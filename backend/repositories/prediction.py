from sqlalchemy.orm import Session
from typing import Optional
from models.prediction import Prediction

def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[Prediction]:
    """Retrieves a single prediction audit log by its primary key."""
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()

def get_prediction_by_transaction_id(db: Session, transaction_id: int) -> Optional[Prediction]:
    """Retrieves prediction metadata linked to a transaction ID."""
    return db.query(Prediction).filter(Prediction.transaction_id == transaction_id).first()

def create_prediction(
    db: Session,
    transaction_id: int,
    probability: float,
    decision: str,
    features: dict,
    model_version: str = "1.0.0"
) -> Prediction:
    """
    Creates and records a model prediction audit record, calculating
    the visual risk score (probability * 100).
    """
    risk_score = float(probability * 100.0)
    db_pred = Prediction(
        transaction_id=transaction_id,
        probability=float(probability),
        risk_score=risk_score,
        decision=decision,
        features=features,
        model_version=model_version
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred
