# Import necessary modules and classes
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Import modules from the app module
from app import services, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash, verify_password_reset_token

# Create an instance of APIRouter
router = APIRouter()

# Define a FastAPI endpoint for token login


@router.post("/login/access-token", response_model=schemas.LoginResponse)
def login_access_token(
    form_data: schemas.LoginPayload,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Parameters:
    - form_data: Pydantic model for login payload.
    - db: The database session (injected dependency).

    Returns:
    - A dictionary containing user information and authentication details.
    """
    user = services.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Email o contraseña incorrecta")

    # CREATE TOKEN
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        {"sub": user.username}, expires_delta=access_token_expires
    )

    login_response = schemas.LoginResponse(
        user=schemas.UserResponse(username=user.username),
        auth=schemas.Token(
            accessToken=access_token,
            tokenType="bearer"
        )
    )
    return login_response

# Define a FastAPI endpoint to test the token


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test the authentication token.

    Parameters:
    - current_user: The current authenticated user (injected dependency).

    Returns:
    - User information.
    """
    return current_user

# Define a FastAPI endpoint to reset the password
@router.post("/reset-password/", response_model=schemas.ApiResponse)
def reset_password(
    authorization: str = Header(...),
    db: Session = Depends(deps.get_db),
    new_password: str = Body(...),
    confirm_password: str = Body(...),
    authenticated: models.User = Depends(deps.get_current_authenticated_user),
) -> Any:
    """
    Reset password.

    Parameters:
    - token: The password reset token.
    - new_password: The new password.
    - db: The database session (injected dependency).
    - authenticated: The currently authenticated user (injected dependency).

    Returns:
    - A message indicating the success of the password update.
    """
    _, token = authorization.split()
    username = verify_password_reset_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="El token es inválido.")
    _ = services.user._update_password(db,user=authenticated,confirm_password=confirm_password,new_password=new_password)
    return schemas.ApiResponse(message="Contraseña Actualizada Correctamente", status=200)