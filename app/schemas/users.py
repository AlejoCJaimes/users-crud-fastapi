from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    fullname: str
    username: str
    email: str
    password_hash: str
    is_authenticated: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_blocked: Optional[bool] = False

class UserCreate(UserBase):
    username: str

class UserUpdate(BaseModel):
    """Properties to receive via API on user update."""
    attempts_login_failed: Optional[int] = 0
    password_hash: Optional[str] = None
    fullname: Optional[str] = None
    username: Optional[str] = None
    is_authenticated: Optional[bool] = False
    is_blocked: Optional[bool] = False
    
class User(UserBase):
    id: int

    class Config:
        from_attributes = True
