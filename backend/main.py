"""
PyAssistant Analytics - Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import logging

from config import settings
from database import init_db
from api import activities, analytics, chat

# Logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup, cleanup on shutdown."""
    logger.info("Starting PyAssistant Analytics...")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown logic (if any) goes here
    logger.info("Shutting down PyAssistant Analytics...")


# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Dashboard personal de productividad con IA - Built by Iván Arias",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "ai_enabled": settings.GEMINI_API_KEY != "your_gemini_api_key_here",
    }


@app.get("/api/info", tags=["System"])
async def app_info():
    """Application information"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "author": "Iván Arias G.",
        "linkedin": "https://linkedin.com/in/ivan-arias-993587233",
        "github": "https://github.com/IvanArias77",
        "stack": {
            "backend": "FastAPI",
            "database": "SQLite",
            "ai": "Google Gemini",
            "frontend": "Vanilla JS + Chart.js",
        },
    }


# Include routers
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])

# Static files (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """Serve the frontend dashboard"""
        return FileResponse(str(frontend_path / "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )