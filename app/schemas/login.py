from pydantic import BaseModel

class UserResponse(BaseModel):
    """Pydantic schema for a user."""
    username: str

class Token(BaseModel):
    """Pydantic schema for a token."""
    accessToken: str
    tokenType: str

class TokenPayload(BaseModel):
    """Pydantic schema for a token payload."""
    sub: str

class LoginResponse(BaseModel):
    """Pydantic schema for a login response."""
    user: UserResponse
    auth: Token


class LoginPayload(BaseModel):
    """Pydantic schema for the login payload."""
    username: str
    password: str