"""
Activity model - Core entity for tracking time.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    duration_minutes = Column(Float, nullable=False)  # in minutes
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    end_time = Column(DateTime, nullable=True)
    productivity_score = Column(Integer, nullable=True)  # 1-10 self-assessment
    tags = Column(String(500), nullable=True)  # comma-separated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    category = relationship("Category", back_populates="activities")

    def __repr__(self):
        return f"<Activity(id={self.id}, title='{self.title}', duration={self.duration_minutes}min)>"