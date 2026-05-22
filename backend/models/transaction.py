from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Attributed user
    card_number = Column(String, nullable=False) # Masked card number: e.g. XXXX-XXXX-XXXX-1234
    amount = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    status = Column(String, default="APPROVED", nullable=False) # APPROVED, REVIEW, BLOCKED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    prediction = relationship("Prediction", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
