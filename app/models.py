from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base
import uuid

class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")
    is_completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )