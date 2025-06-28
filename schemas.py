from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from models import TaskStatus, TaskPriority

# A Pydantic model used for creating a new task
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        max_length=200
        )
    description: Optional[str] = Field(
        None,
        max_length=1000
        )
    status: TaskStatus = Field(
        default=TaskStatus.pending
    )
    priority: TaskPriority = Field(
        default=TaskPriority.medium
    )
    due_date: Optional[datetime] = Field(
        default=None
    )
    assigned_to: Optional[str] = Field(
        None,
        max_length=100
    )
    # Validator to ensure title is not just whitespace
    @field_validator('title')
    @classmethod
    def title_validation(cls, value:str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title must not be empty or only whitespace")
        return value
    # Validator to ensure due date is in the future
    @field_validator('due_date')
    @classmethod
    def date_validation(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return value
    
# A Pydantic model used for updating an existing task (all fields are optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        max_length=200
    )
    description: Optional[str] = Field(
        None,
        max_length=1000
    )
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(
        None,
        max_length=100
    )
    @field_validator('title')
    @classmethod
    def title_validation(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Title must not be empty or only whitespace")
        return value
    
    @field_validator('due_date')
    @classmethod
    def date_validation(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return value
    
# A Pydantic model used to structure API responses
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]
    
    class Config:
        from_attributes = True