"""Basic tests for the API."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base


# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data


def test_app_info(client):
    """Test info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PyAssistant Analytics"
    assert "stack" in data


def test_create_category(client):
    """Test creating a category"""
    response = client.post("/api/activities/categories/?name=TestCategory&color=%23FF0000&icon=🎯")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestCategory"
    assert "id" in data


def test_list_categories(client):
    """Test listing categories"""
    response = client.get("/api/activities/categories/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_activity(client):
    """Test creating an activity"""
    # First get a category
    categories = client.get("/api/activities/categories/all").json()
    if not categories:
        client.post("/api/activities/categories/?name=TestCat&color=%230000FF")
        categories = client.get("/api/activities/categories/all").json()

    category_id = categories[0]["id"]

    activity_data = {
        "title": "Test Activity",
        "description": "Test description",
        "category_id": category_id,
        "duration_minutes": 60.0,
        "start_time": "2025-01-15T10:00:00",
        "productivity_score": 8,
    }

    response = client.post("/api/activities/", json=activity_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Activity"
    assert data["category_id"] == category_id


def test_list_activities(client):
    """Test listing activities"""
    response = client.get("/api/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_analytics_summary(client):
    """Test analytics summary endpoint"""
    response = client.get("/api/analytics/summary?days=30")
    assert response.status_code == 200
    data = response.json()
    assert "total_activities" in data
    assert "total_hours" in data


def test_analytics_daily(client):
    """Test daily analytics"""
    response = client.get("/api/analytics/daily?days=7")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_analytics_by_category(client):
    """Test category analytics"""
    response = client.get("/api/analytics/by-category?days=30")
    assert response.status_code == 200
    assert isinstance(response.json(), list)