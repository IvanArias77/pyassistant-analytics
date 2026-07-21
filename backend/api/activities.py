"""
Activities API endpoints - CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Activity, Category
from schemas import ActivityCreate, ActivityUpdate, ActivityResponse

router = APIRouter()


@router.get("/", response_model=List[ActivityResponse])
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """
    List activities with optional filters.

    - **skip**: Pagination offset
    - **limit**: Max items (1-500)
    - **category_id**: Filter by category
    - **start_date**: Filter activities from this date
    - **end_date**: Filter activities until this date
    """
    query = db.query(Activity)

    if category_id:
        query = query.filter(Activity.category_id == category_id)
    if start_date:
        query = query.filter(Activity.start_time >= start_date)
    if end_date:
        query = query.filter(Activity.start_time <= end_date)

    activities = query.order_by(desc(Activity.start_time)).offset(skip).limit(limit).all()

    # Enrich with category info
    result = []
    for activity in activities:
        activity_dict = ActivityResponse.model_validate(activity).model_dump()
        activity_dict["category_name"] = activity.category.name if activity.category else None
        activity_dict["category_color"] = activity.category.color if activity.category else None
        result.append(activity_dict)

    return result


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new activity.
    """
    # Verify category exists
    category = db.query(Category).filter(Category.id == activity.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {activity.category_id} not found")

    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    response = ActivityResponse.model_validate(db_activity).model_dump()
    response["category_name"] = category.name
    response["category_color"] = category.color

    return response


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    response = ActivityResponse.model_validate(activity).model_dump()
    response["category_name"] = activity.category.name
    response["category_color"] = activity.category.color
    return response


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing activity."""
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_data = activity_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_activity, key, value)

    db.commit()
    db.refresh(db_activity)

    response = ActivityResponse.model_validate(db_activity).model_dump()
    response["category_name"] = db_activity.category.name
    response["category_color"] = db_activity.category.color
    return response


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
):
    """Delete an activity."""
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    db.delete(db_activity)
    db.commit()
    return None


# Category endpoints (nested here for simplicity)
@router.get("/categories/all", response_model=List[dict])
async def list_categories(db: Session = Depends(get_db)):
    """List all categories."""
    categories = db.query(Category).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "color": c.color,
            "icon": c.icon,
            "description": c.description,
            "activity_count": len(c.activities),
        }
        for c in categories
    ]


@router.post("/categories/", status_code=201)
async def create_category(
    name: str,
    color: str = "#3B82F6",
    icon: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Create a new category."""
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Category '{name}' already exists")

    category = Category(name=name, color=color, icon=icon, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return {"id": category.id, "name": category.name, "color": category.color}