from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from core.database import get_db
from schemas.transaction import TransactionCreate, TransactionResponse
from services.risk_engine import risk_engine_service
from services.transaction import transaction_service
from api.deps import get_current_user, requires_admin
from models.user import User
from models.transaction import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/predict", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def predict_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits a transaction for fraud risk prediction.
    Applies standard ML preprocessing, performs inference, saves results, and returns status.
    """
    return risk_engine_service.process_transaction(
        db=db, transaction_in=transaction_in, user_id=current_user.id
    )

@router.get("/history", response_model=List[TransactionResponse])
def get_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves transaction histories.
    - Admins see global system logs.
    - Standard Users see only their own transactions.
    """
    user_id = None if current_user.role == "admin" else current_user.id
    return transaction_service.get_transaction_history(
        db=db, skip=skip, limit=limit, user_id=user_id
    )

@router.get("/metrics", response_model=Dict[str, Any])
def get_system_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Calculates key telemetry aggregates for the frontend dashboard:
    - Total Transaction Count
    - APPROVED, REVIEW, BLOCKED transaction breakdowns
    - Total Volume processed
    - Overall flagged Fraud rate
    """
    # Scope metrics to user unless admin
    user_id = None if current_user.role == "admin" else current_user.id
    txns = transaction_service.get_transaction_history(db=db, limit=1000, user_id=user_id)
    
    total_txns = len(txns)
    approved = sum(1 for t in txns if t.status == "APPROVED")
    review = sum(1 for t in txns if t.status == "REVIEW")
    blocked = sum(1 for t in txns if t.status == "BLOCKED")
    total_amount = sum(t.amount for t in txns)
    
    fraud_rate = (blocked / total_txns * 100.0) if total_txns > 0 else 0.0
    
    # Calculate amount distributions
    status_distribution = [
        {"name": "Approved", "value": approved},
        {"name": "Review", "value": review},
        {"name": "Blocked", "value": blocked}
    ]
    
    return {
        "total_count": total_txns,
        "approved_count": approved,
        "review_count": review,
        "blocked_count": blocked,
        "total_amount": round(total_amount, 2),
        "fraud_rate_pct": round(fraud_rate, 2),
        "status_distribution": status_distribution
    }

@router.patch("/{id}/override", response_model=TransactionResponse)
def override_transaction_status(
    id: int,
    target_status: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(requires_admin)
):
    """
    Allows administrators to manually approve or block flagged transactions (e.g. during compliance reviews).
    Requires the 'admin' security role.
    """
    return transaction_service.manual_override(db=db, transaction_id=id, target_status=target_status)
