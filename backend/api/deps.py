from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Generator

from core.config import settings
from core.database import get_db
from models.user import User
from repositories import user_repository
from schemas.auth import TokenData

# Use HTTPBearer for clean bearer authorization
security_scheme = HTTPBearer()

def get_current_user(
    db: Session = Depends(get_db),
    token_credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> User:
    """
    Extracts the authorization token, decodes JWT claims,
    and returns the authenticated user object.
    Raises 401 UNAUTHORIZED if token is invalid or expired.
    """
    token = token_credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
        
    user = user_repository.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def requires_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency checking that the authenticated user possesses the 'admin' authorization role.
    Raises 403 FORBIDDEN if the user's role is insufficient.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Administrative privileges are required for this action."
        )
    return current_user
