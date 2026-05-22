from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

class PredictionResponse(BaseModel):
    id: int
    transaction_id: int
    probability: float
    risk_score: float
    decision: str
    features: Optional[Dict[str, Any]] = None
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True
