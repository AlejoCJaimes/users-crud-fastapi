from pydantic import BaseModel
from typing import Optional

class ApiResponse(BaseModel):
    message: Optional[str]
    status: int