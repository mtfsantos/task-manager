from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from app.core.config import settings
from jose import jwt


# Mocked user and token generation for demonstration
# In a real app, this would involve hashing passwords, JWT encoding/decoding

MOCKED_USER_DB = {
    "user": {
        "username": "user",
        "password": "password"  # Plain text for mock. NEVER do this in production.
    }
}

def authenticate_user_mocked(username: str, password: str) -> Optional[dict]:
    """
    Simulates user authentication against a mocked database.
    """
    user = MOCKED_USER_DB.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an access token using JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    """
    Verifies an access token and returns the payload if valid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return {"username": username}
    except jwt.JWTError:
        return None
