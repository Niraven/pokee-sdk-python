"""Data models for the Pokee SDK."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Possible states of a task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    """Represents a Pokee task."""

    id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Human-readable task name")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    skill: str = Field(..., description="Skill used for this task")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Dict[str, Any]] = Field(default=None)
    error: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class TaskList(BaseModel):
    """Paginated list of tasks."""

    tasks: List[Task] = Field(default_factory=list)
    total: int = Field(default=0)
    page: int = Field(default=1)
    per_page: int = Field(default=20)
    has_more: bool = Field(default=False)


class Skill(BaseModel):
    """Represents an available Pokee skill."""

    id: str
    name: str
    description: str
    category: str
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)
    is_available: bool = Field(default=True)


class SkillList(BaseModel):
    """List of available skills."""

    skills: List[Skill] = Field(default_factory=list)
    total: int = Field(default=0)
