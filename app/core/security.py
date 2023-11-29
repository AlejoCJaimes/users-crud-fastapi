
from datetime import datetime,timedelta
from typing import Any, Union, Optional

from jose import jwt
import json
from app.core.config import settings
from passlib.context import CryptContext

# CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWT algorithm
ALGORITHM = settings.ALGORITHM


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        sub_dict = decoded_token['sub'].replace("'", "\"")
        sub_dict = json.loads(sub_dict)
        return sub_dict['sub']
    except jwt.JWTError:
        return None