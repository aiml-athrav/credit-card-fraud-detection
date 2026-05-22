from sqlalchemy.orm import Session
from typing import Optional
from models.user import User
from schemas.auth import UserRegister
from core.security import get_password_hash

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieves a user record by primary key."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieves a user record by username (case-insensitive for safety)."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieves a user record by email address."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserRegister) -> User:
    """Creates and commits a new user with salted bcrypt password hashing."""
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
