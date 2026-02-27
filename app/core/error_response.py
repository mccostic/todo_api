from pydantic import BaseModel
from typing import Optional, Any, Dict

class ErrorResponse(BaseModel):
    code: int
    message: str
    details: Optional[str] = None
    errors: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None