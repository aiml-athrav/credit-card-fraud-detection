from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Credit Card Fraud Detection System"
    
    # JWT security credentials
    SECRET_KEY: str = "CREDIT_CARD_FRAUD_SYSTEM_JWT_SECRET_SIGNING_KEY_2026_522"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours (1 day)
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "*"]
    
    class Config:
        case_sensitive = True

settings = Settings()
