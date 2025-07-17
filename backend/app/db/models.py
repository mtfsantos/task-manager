import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.sql import func
import enum

from sqlalchemy_utils import UUIDType 

from app.db.base import Base

class TaskStatusEnum(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
