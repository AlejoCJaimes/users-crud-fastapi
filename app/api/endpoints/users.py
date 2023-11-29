# Import necessary modules and classes
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, services
from app.api import deps
from app import services

# Create an instance of APIRouter
router = APIRouter()

# Define a FastAPI endpoint to list users


@router.get("/", response_model=List[schemas.User])
def list_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve users.

    Parameters:
    - db: The database session (injected dependency).
    - skip: Number of items to skip in the result.
    - limit: Maximum number of items to retrieve.
    - authenticated: The authenticated user (injected dependency).
    - current_user: The current active superuser (injected dependency).

    Returns:
    - A list of user data.
    """
    users = services.user.get_multi(db, skip=skip, limit=limit)
    return users

# Define a FastAPI endpoint to create a new user


@router.post("/", response_model=schemas.ApiResponse)
def create_user(
    userCreate: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.

    Parameters:
    - userCreate: The data for creating a new user.
    - db: The database session (injected dependency).
    - authenticated: The authenticated user (injected dependency).
    - current_user: The current active superuser (injected dependency).

    Returns:
    - The created user data.
    """
    user = services.user.get_by_email(db, email=userCreate.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="El usuario con ese nombre, ya existe.",
        )
    else:
        obj_create = services.user.create(db, user=userCreate)
        return schemas.ApiResponse(message=f'Usuario {obj_create.username} creado correctamente', status=200)
    

   

# Define a FastAPI endpoint to update a user
@router.put("/{user_id}", response_model=schemas.ApiResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    user_in: schemas.UserUpdate,
    authenticated: models.User = Depends(deps.get_current_authenticated_user),
) -> Any:
    """
    Update a user.

    Parameters:
    - db: The database session (injected dependency).
    - user_id: The ID of the user to update.
    - user_in: The data for updating the user.
    - authenticated: The authenticated user (injected dependency).

    Returns:
    - The updated user data.
    """
    user = services.user.get(db, id=id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="El usuario con ese nombre, ya existe.",
        )
    user = services.user.update(db, db_obj=user, obj_in=user_in)
    return schemas.ApiResponse(message=f'Usuario {user.username} actualizado correctamente', status=200)


# Define a FastAPI endpoint to update a user
@router.post("/{user_id}", response_model=schemas.ApiResponse)
def unlock_account(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.

    Parameters:
    - db: The database session (injected dependency).
    - user_id: The ID of the user to update.
    - user_in: The data for updating the user.
    - authenticated: The authenticated user (injected dependency).

    Returns:
    - The updated user data.
    """
    user = services.user.get(db, id=id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"El usuario no existe",
        )
    user_unlock = services.user._unlock_account(db, user=user)
    return schemas.ApiResponse(message=f'Usuario {user_unlock.username} desbloqueado correctamente,', status=200)


@router.delete("/{id}", response_model=schemas.ApiResponse)
def delete_user(
    db: Session = Depends(deps.get_db),
    id: Optional[int] = 0,
    #current_user: models.User = Depends(deps.get_current_active_superuser),
    ):
    """
    Delete an user.
    """
    user = services.user.get_by_id(db, id=id)
    if user == None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_delete = services.user._remove_user(db,user)
    return schemas.ApiResponse(message=f'Usuario {user_delete} eliminado correctamente', status=200)