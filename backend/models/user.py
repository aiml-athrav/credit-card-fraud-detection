from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False) # 'admin' or 'user'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to transactions submitted/processed by this user
    transactions = relationship("Transaction", back_populates="user")
