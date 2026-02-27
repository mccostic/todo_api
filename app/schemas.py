from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

    # Validate title not empty
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}