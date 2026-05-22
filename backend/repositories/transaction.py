from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from models.transaction import Transaction

def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    """Retrieves a single transaction by primary key."""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_transactions(
    db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
) -> List[Transaction]:
    """
    Retrieves a list of transactions, optionally filtered by user_id
    and sorted by execution timestamp descending.
    """
    query = db.query(Transaction)
    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)
    return query.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()

def create_transaction(
    db: Session,
    amount: float,
    card_number: str,
    merchant: str,
    status: str = "APPROVED",
    user_id: Optional[int] = None
) -> Transaction:
    """
    Creates and saves a new transaction in the database.
    Masks the input credit card number automatically to safeguard sensitive financial info.
    """
    # Auto-mask card number (e.g. keep last 4 digits only)
    cleaned_card = "".join(c for c in card_number if c.isdigit())
    masked_card = f"XXXX-XXXX-XXXX-{cleaned_card[-4:]}" if len(cleaned_card) >= 4 else "XXXX-XXXX-XXXX-XXXX"
    
    db_txn = Transaction(
        user_id=user_id,
        card_number=masked_card,
        amount=amount,
        merchant=merchant,
        status=status,
        created_at=datetime.utcnow()
    )
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn

def update_transaction_status(
    db: Session, transaction_id: int, status: str
) -> Optional[Transaction]:
    """
    Updates the evaluation status of a transaction (e.g. manual compliance overrides).
    """
    db_txn = get_transaction_by_id(db, transaction_id)
    if db_txn:
        db_txn.status = status
        db.commit()
        db.refresh(db_txn)
    return db_txn
