from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from models.transaction import Transaction
from repositories import transaction_repository

class TransactionService:
    """
    Service layer representing post-prediction credit card operations and history.
    """
    
    def get_transaction(self, db: Session, transaction_id: int) -> Transaction:
        """Retrieves a single transaction, throwing 404 if not found."""
        txn = transaction_repository.get_transaction_by_id(db, transaction_id)
        if not txn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} not found."
            )
        return txn

    def get_transaction_history(
        self, db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[Transaction]:
        """Retrieves history, supporting optional user scoping."""
        return transaction_repository.get_transactions(db, skip=skip, limit=limit, user_id=user_id)

    def manual_override(self, db: Session, transaction_id: int, target_status: str) -> Transaction:
        """
        Enables administrators to override predictions (e.g. approving a REVIEW flag).
        Valid target statuses are: APPROVED, REVIEW, BLOCKED.
        """
        if target_status not in ["APPROVED", "REVIEW", "BLOCKED"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid target status '{target_status}'. Must be APPROVED, REVIEW, or BLOCKED."
            )
            
        txn = transaction_repository.update_transaction_status(db, transaction_id, target_status)
        if not txn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} not found."
            )
        return txn

transaction_service = TransactionService()
