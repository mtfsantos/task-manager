from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

from app.db.models import TaskStatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatusEnum = Field(TaskStatusEnum.PENDING)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatusEnum] = None

class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID 
    created_at: datetime
    updated_at: Optional[datetime]