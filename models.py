from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

# Enum to represent possible task status
class TaskStatus(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

# Enum to represent task priority levels
class TaskPriority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    urgent = 'urgent'
    
# Main Task model mapped to the database using SQLModel
class Task(SQLModel, table=True):
    # Unique identifier for each task (auto-incremented primary key)
    id: Optional[int]=Field(
        default=None,
        primary_key=True,
        description='Unique task identifier'
        )
    # Title of the task (required, max 200 characters)
    title: str = Field(
        max_length=200,
        description='Task title'
        )
    # Optional task description (up to 1000 characters)
    description: Optional[str]=Field(
        default=None,
        max_length=1000,
        description='Task description'
        )
    # Task status (default: pending)
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description='Task status'
        )
    # Task priority (default: medium)
    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        description='Task priority'
        )
    # Timestamp when the task was created (auto-generated)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description='Creation timestamp'
    )
    # Optional timestamp for when the task was last updated
    updated_at: Optional[datetime] = Field(
        default=None,
        description='Last update timestamp'
    )
    # Optional due date for the task
    due_date: Optional[datetime] = Field(
        default=None,
        description='Task deadline'
    )
    # Optional name of the person assigned to the task
    assigned_to: Optional[str] = Field(
        default=None,
        max_length=100,
        description='Assignee name'
    )