from fastapi import APIRouter
from app.api.endpoints import (
    users,login
)
endpoints = [
    (login.router, "/auth", "Authentication"),
    (users.router, "/users", "Users"),
]


api_router = APIRouter()

for router, prefix, tags in endpoints:
    api_router.include_router(router, prefix=prefix, tags=[tags])
