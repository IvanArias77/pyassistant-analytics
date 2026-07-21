"""
Chat API endpoints - AI-powered conversational interface.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import Activity, Category
from ai import generate_insights, answer_question, is_ai_enabled

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    days: Optional[int] = 30


class InsightsRequest(BaseModel):
    days: Optional[int] = 30


def _prepare_context(db: Session, days: int) -> dict:
    """Prepare activity data as context for AI."""
    start_date = datetime.utcnow() - timedelta(days=days)

    activities = db.query(Activity).filter(Activity.start_time >= start_date).all()

    if not activities:
        return {"error": "No activities found in the specified period"}

    total_minutes = sum(a.duration_minutes for a in activities)
    scores = [a.productivity_score for a in activities if a.productivity_score]

    # By category
    cat_stats = (
        db.query(
            Category.name,
            func.count(Activity.id).label("count"),
            func.sum(Activity.duration_minutes).label("minutes"),
        )
        .join(Activity, Activity.category_id == Category.id)
        .filter(Activity.start_time >= start_date)
        .group_by(Category.name)
        .all()
    )

    return {
        "period_days": days,
        "total_activities": len(activities),
        "total_hours": round(total_minutes / 60, 2),
        "average_productivity_score": round(sum(scores) / len(scores), 2) if scores else None,
        "by_category": [
            {
                "category": c.name,
                "count": c.count,
                "hours": round(c.minutes / 60, 2) if c.minutes else 0,
            }
            for c in cat_stats
        ],
    }


@router.post("/ask")
async def ask_question(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Ask a natural language question about your activity data.

    The AI will analyze your activities and provide a contextual answer.
    """
    if not is_ai_enabled():
        raise HTTPException(
            status_code=503,
            detail="AI features are not configured. Please add GEMINI_API_KEY to your .env file.",
        )

    context = _prepare_context(db, request.days)
    answer = await answer_question(request.question, context)

    return {
        "question": request.question,
        "answer": answer,
        "context_period_days": request.days,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("/insights")
async def get_insights(
    request: InsightsRequest,
    db: Session = Depends(get_db),
):
    """
    Get AI-generated insights about your productivity patterns.
    """
    if not is_ai_enabled():
        raise HTTPException(
            status_code=503,
            detail="AI features are not configured. Please add GEMINI_API_KEY to your .env file.",
        )

    context = _prepare_context(db, request.days)
    insights = await generate_insights(context)

    return {
        "insights": insights,
        "period_days": request.days,
        "generated_at": datetime.utcnow().isoformat(),
    }