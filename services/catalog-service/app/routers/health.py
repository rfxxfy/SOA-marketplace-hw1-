from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings
from app.database import engine

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    db_status = "ok"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "service": settings.app_name,
        "database": db_status,
    }
