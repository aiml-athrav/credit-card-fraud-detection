from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="CASCADE"), unique=True, nullable=False)
    probability = Column(Float, nullable=False) # raw decimal 0.0 - 1.0
    risk_score = Column(Float, nullable=False) # scaled 0 - 100 for visual dashboards
    decision = Column(String, nullable=False) # APPROVED, REVIEW, BLOCKED
    features = Column(JSON, nullable=True) # full V1-V28, Time, Amount dump for explainability/audits
    model_version = Column(String, default="1.0.0", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="prediction")
