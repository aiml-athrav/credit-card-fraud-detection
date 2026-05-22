from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Dict, Any
from schemas.prediction import PredictionResponse

class TransactionCreate(BaseModel):
    card_number: str = Field(..., min_length=12, max_length=19, description="16-digit credit card number")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    merchant: str = Field(..., min_length=1, max_length=100)
    profile: Optional[str] = Field("genuine", pattern=r"^(genuine|suspicious|fraudulent)$", description="Simulation profile for model evaluation")
    features: Optional[Dict[str, float]] = Field(None, description="Optional raw V1-V28 PCA features")

    @field_validator('card_number')
    def validate_card_number(cls, v):
        # Strip dashes and spaces
        cleaned = "".join(c for c in v if c.isdigit())
        if len(cleaned) < 12 or len(cleaned) > 19:
            raise ValueError("Card number must contain between 12 and 19 digits")
        return cleaned

class TransactionResponse(BaseModel):
    id: int
    card_number: str
    amount: float
    merchant: str
    status: str
    created_at: datetime
    prediction: Optional[PredictionResponse] = None

    class Config:
        from_attributes = True
