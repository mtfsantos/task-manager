from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserOut, Token  # Assuming Token schema for response
from app.core.security import authenticate_user_mocked, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Mocked user login endpoint.
    Authenticates a user with fixed credentials and returns a mocked token.
    """
    user = authenticate_user_mocked(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real application, generate a JWT here
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}