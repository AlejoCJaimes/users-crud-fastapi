from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # SOFTWARE CONFIGURATION
    API_V1_STR: str = "/api/v1"
    OPEN_API_DOC: str = "openapi.json"
    PROJECT_NAME: str = "USERS-CRUD"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    ATTEMPTS_LOGIN_FAILED: int = os.environ.get("ATTEMPTS_LOGIN_FAILED")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173",
                                              "https://main.d2j023puzmxhn6.amplifyapp.com", "https://main.d1bn33etsekcyp.amplifyapp.com"]
    # DATABASE CONFIGURATION
    DB_HOST: str =  os.environ.get("DB_HOST")
    DB_USER: str =  os.environ.get("DB_USER")
    DB_PASSWORD: str =  os.environ.get("DB_PASSWORD")
    DB_NAME: str =  os.environ.get("DB_NAME")
    DB_PORT: int =  os.environ.get("DB_PORT")
    DATABASE_URL: str = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    class Config:
        case_sensitive = True

settings = Settings()