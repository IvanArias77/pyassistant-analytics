"""
Analytics API endpoints - Aggregations and statistics.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import Activity, Category

router = APIRouter()


@router.get("/summary")
async def get_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
):
    """
    Get overall summary statistics.

    Returns total activities, total time, average productivity score,
    and most productive day.
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    activities = db.query(Activity).filter(Activity.start_time >= start_date).all()

    if not activities:
        return {
            "period_days": days,
            "total_activities": 0,
            "total_hours": 0,
            "average_productivity": 0,
            "most_productive_day": None,
            "message": "No activities found in this period",
        }

    total_minutes = sum(a.duration_minutes for a in activities)
    scores = [a.productivity_score for a in activities if a.productivity_score]
    avg_score = sum(scores) / len(scores) if scores else 0

    # Group by day
    daily_hours = {}
    for a in activities:
        day = a.start_time.strftime("%Y-%m-%d")
        daily_hours[day] = daily_hours.get(day, 0) + a.duration_minutes / 60

    most_productive_day = max(daily_hours.items(), key=lambda x: x[1])

    return {
        "period_days": days,
        "total_activities": len(activities),
        "total_hours": round(total_minutes / 60, 2),
        "average_productivity": round(avg_score, 2),
        "most_productive_day": {
            "date": most_productive_day[0],
            "hours": round(most_productive_day[1], 2),
        },
        "daily_average_hours": round((total_minutes / 60) / days, 2),
    }


@router.get("/daily")
async def get_daily_metrics(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
):
    """Get daily metrics for the last N days."""
    start_date = datetime.utcnow() - timedelta(days=days)
    activities = db.query(Activity).filter(Activity.start_time >= start_date).all()

    daily_data = {}
    for i in range(days):
        day = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_data[day] = {"date": day, "hours": 0, "activities": 0, "avg_score": 0}

    for activity in activities:
        day = activity.start_time.strftime("%Y-%m-%d")
        if day in daily_data:
            daily_data[day]["hours"] += activity.duration_minutes / 60
            daily_data[day]["activities"] += 1
            if activity.productivity_score:
                current = daily_data[day]["avg_score"]
                count = daily_data[day]["activities"]
                daily_data[day]["avg_score"] = (
                    (current * (count - 1) + activity.productivity_score) / count
                )

    result = []
    for day_data in daily_data.values():
        day_data["hours"] = round(day_data["hours"], 2)
        day_data["avg_score"] = round(day_data["avg_score"], 2)
        result.append(day_data)

    return sorted(result, key=lambda x: x["date"])


@router.get("/by-category")
async def get_by_category(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """Get time distribution by category."""
    start_date = datetime.utcnow() - timedelta(days=days)
    results = (
        db.query(
            Category.id,
            Category.name,
            Category.color,
            Category.icon,
            func.count(Activity.id).label("count"),
            func.sum(Activity.duration_minutes).label("total_minutes"),
            func.avg(Activity.productivity_score).label("avg_score"),
        )
        .join(Activity, Activity.category_id == Category.id)
        .filter(Activity.start_time >= start_date)
        .group_by(Category.id)
        .all()
    )

    return [
        {
            "category_id": r.id,
            "name": r.name,
            "color": r.color,
            "icon": r.icon,
            "activity_count": r.count,
            "total_hours": round(r.total_minutes / 60, 2) if r.total_minutes else 0,
            "average_productivity": round(r.avg_score, 2) if r.avg_score else 0,
        }
        for r in results
    ]


@router.get("/weekly")
async def get_weekly_metrics(
    weeks: int = Query(4, ge=1, le=12),
    db: Session = Depends(get_db),
):
    """Get weekly aggregated metrics."""
    start_date = datetime.utcnow() - timedelta(weeks=weeks)
    activities = db.query(Activity).filter(Activity.start_time >= start_date).all()

    weekly_data = {}
    for activity in activities:
        # Get ISO week
        year, week_num, _ = activity.start_time.isocalendar()
        key = f"{year}-W{week_num:02d}"
        if key not in weekly_data:
            weekly_data[key] = {"week": key, "hours": 0, "activities": 0}
        weekly_data[key]["hours"] += activity.duration_minutes / 60
        weekly_data[key]["activities"] += 1

    result = []
    for week_data in weekly_data.values():
        week_data["hours"] = round(week_data["hours"], 2)
        result.append(week_data)

    return sorted(result, key=lambda x: x["week"])