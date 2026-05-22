from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from schemas.auth import UserRegister, UserLogin, Token
from repositories import user_repository
from core.security import verify_password, create_access_token
from models.user import User

class AuthService:
    """
    Service layer governing user identity, access controls, and password validation.
    """
    def register_user(self, db: Session, user_in: UserRegister) -> User:
        """
        Registers a new user, verifying username and email uniqueness.
        """
        # Check username uniqueness
        existing_user = user_repository.get_user_by_username(db, user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists."
            )
            
        # Check email uniqueness
        existing_email = user_repository.get_user_by_email(db, user_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )
            
        return user_repository.create_user(db, user_in)

    def authenticate_user(self, db: Session, credentials: UserLogin) -> Token:
        """
        Validates login credentials, producing secure JWT access tokens.
        Supports fallback matching on username.
        """
        user = user_repository.get_user_by_username(db, credentials.username)
        if not user:
            # Try looking up by email in case they logged in with email
            user = user_repository.get_user_by_email(db, credentials.username)
            
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        # Create token payload containing identity and access role
        access_token = create_access_token(subject=user.username, role=user.role)
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role,
            username=user.username
        )

auth_service = AuthService()
