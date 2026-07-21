"""
Seed data script - Generates example activities for demo purposes.

Usage:
    cd backend
    python -m data.seed
"""
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal, init_db
from models import Activity, Category


CATEGORIES = [
    {"name": "Coding", "color": "#3B82F6", "icon": "💻", "description": "Software development"},
    {"name": "Meetings", "color": "#F59E0B", "icon": "🤝", "description": "Team meetings and calls"},
    {"name": "Learning", "color": "#10B981", "icon": "📚", "description": "Courses, reading, research"},
    {"name": "Automation", "color": "#8B5CF6", "icon": "⚙️", "description": "Scripts, bots, tools"},
    {"name": "Data Analysis", "color": "#06B6D4", "icon": "📊", "description": "SQL, dashboards, KPIs"},
    {"name": "AI/ML", "color": "#EC4899", "icon": "🤖", "description": "LLMs, agents, models"},
    {"name": "Planning", "color": "#F97316", "icon": "📋", "description": "Strategy, planning, docs"},
    {"name": "Administrative", "color": "#6B7280", "icon": "📝", "description": "Email, reports, admin"},
]

ACTIVITIES = [
    # Coding
    {"title": "Desarrollo de dashboard FastAPI", "category": "Coding", "scores": [7, 8, 9]},
    {"title": "Refactor de código Python", "category": "Coding", "scores": [6, 7]},
    {"title": "Code review del equipo", "category": "Coding", "scores": [7, 8]},
    {"title": "Implementación de API REST", "category": "Coding", "scores": [8, 9]},

    # Meetings
    {"title": "Daily standup", "category": "Meetings", "scores": [5, 6]},
    {"title": "Sprint planning", "category": "Meetings", "scores": [6, 7]},
    {"title": "1-on-1 con manager", "category": "Meetings", "scores": [7, 8]},
    {"title": "Reunión con stakeholders", "category": "Meetings", "scores": [5, 6]},

    # Learning
    {"title": "Curso de LangChain", "category": "Learning", "scores": [8, 9, 9]},
    {"title": "Lectura de documentación técnica", "category": "Learning", "scores": [7, 8]},
    {"title": "Tutorial de FastAPI", "category": "Learning", "scores": [8]},
    {"title": "Investigación de multi-agent systems", "category": "Learning", "scores": [9]},

    # Automation
    {"title": "Bot de scraping en Python", "category": "Automation", "scores": [8, 9]},
    {"title": "Script de automatización Excel", "category": "Automation", "scores": [7, 8]},
    {"title": "Configuración de tareas programadas", "category": "Automation", "scores": [6, 7]},

    # Data Analysis
    {"title": "Análisis de KPIs en Power BI", "category": "Data Analysis", "scores": [8, 9]},
    {"title": "Query SQL para reportes", "category": "Data Analysis", "scores": [7, 8]},
    {"title": "Reporte mensual de inventarios", "category": "Data Analysis", "scores": [7, 8]},

    # AI/ML
    {"title": "Diseño de agente con LangGraph", "category": "AI/ML", "scores": [9, 10]},
    {"title": "Experimentación con Gemini API", "category": "AI/ML", "scores": [8, 9]},
    {"title": "Prompt engineering", "category": "AI/ML", "scores": [8, 9]},

    # Planning
    {"title": "Planificación semanal", "category": "Planning", "scores": [7, 8]},
    {"title": "Documentación del proyecto", "category": "Planning", "scores": [6, 7]},

    # Admin
    {"title": "Revisión de emails", "category": "Administrative", "scores": [4, 5]},
    {"title": "Reportes administrativos", "category": "Administrative", "scores": [4, 5]},
]


def seed_database():
    """Populate database with example data."""
    print("🌱 Seeding database...")

    init_db()
    db = SessionLocal()

    try:
        # Clear existing data
        db.query(Activity).delete()
        db.query(Category).delete()
        db.commit()

        # Create categories
        categories = {}
        for cat_data in CATEGORIES:
            category = Category(**cat_data)
            db.add(category)
            db.flush()
            categories[cat_data["name"]] = category

        print(f"✅ Created {len(categories)} categories")

        # Create activities for the last 30 days
        activities_created = 0
        now = datetime.utcnow()

        for days_ago in range(30):
            # Skip some days randomly (weekends less activity)
            date = now - timedelta(days=days_ago)
            if date.weekday() >= 5 and random.random() > 0.3:  # Saturday/Sunday
                continue

            # 3-6 activities per day
            num_activities = random.randint(3, 6)

            for _ in range(num_activities):
                # Random time during work hours (8 AM - 7 PM)
                hour = random.randint(8, 19)
                minute = random.randint(0, 59)
                start_time = date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # Random activity
                activity_template = random.choice(ACTIVITIES)
                category = categories[activity_template["category"]]

                duration = random.choice([30, 45, 60, 90, 120, 150])
                score = random.choice(activity_template["scores"])

                activity = Activity(
                    title=activity_template["title"],
                    description=f"Auto-generated example activity",
                    category_id=category.id,
                    duration_minutes=duration,
                    start_time=start_time,
                    end_time=start_time + timedelta(minutes=duration),
                    productivity_score=score,
                    tags="example,seed",
                )
                db.add(activity)
                activities_created += 1

        db.commit()
        print(f"✅ Created {activities_created} activities across 30 days")
        print(f"\n📊 Summary by category:")

        # Show summary
        for cat_name, cat in categories.items():
            count = db.query(Activity).filter(Activity.category_id == cat.id).count()
            total_min = db.query(func_sum_duration()).filter(Activity.category_id == cat.id).scalar() or 0
            print(f"  {cat.icon} {cat_name}: {count} activities, {total_min/60:.1f}h")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def func_sum_duration():
    from sqlalchemy import func
    return func.sum(Activity.duration_minutes)


if __name__ == "__main__":
    seed_database()
    print("\n🎉 Database seeded successfully!")
    print("🚀 Run the server with: uvicorn main:app --reload")