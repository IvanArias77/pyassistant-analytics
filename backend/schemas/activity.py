"""
Pydantic schemas for Activity.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ActivityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Activity title")
    description: Optional[str] = Field(None, description="Detailed description")
    category_id: int = Field(..., gt=0, description="Category ID")
    duration_minutes: float = Field(..., gt=0, le=1440, description="Duration in minutes (max 24h)")
    start_time: datetime = Field(..., description="When the activity started")
    end_time: Optional[datetime] = Field(None, description="When the activity ended")
    productivity_score: Optional[int] = Field(None, ge=1, le=10, description="Self-assessment 1-10")
    tags: Optional[str] = Field(None, description="Comma-separated tags")


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = Field(None, gt=0)
    duration_minutes: Optional[float] = Field(None, gt=0, le=1440)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    productivity_score: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[str] = None


class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    category_color: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)