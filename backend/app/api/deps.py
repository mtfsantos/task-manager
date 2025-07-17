from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import verify_access_token

# OAuth2PasswordBearer for dependency injection (even if mocked)
# Points to the login endpoint where the token would be obtained
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def get_db() -> Generator:
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to simulate current user authentication.
    """
    user = verify_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user