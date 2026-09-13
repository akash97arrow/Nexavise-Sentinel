from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import SecurityEvent, Alert
from backend.dependencies import get_current_user

from backend.routers.users import router as users_router
from backend.routers.events import router as events_router
from backend.routers.alerts import router as alerts_router

app = FastAPI(title="Nexavise Sentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(users_router)
app.include_router(alerts_router)


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    return {"status": "ok", "message": "SQLAlchemy database session is working"}


@app.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    total_events = db.query(SecurityEvent).count()

    total_alerts = db.query(Alert).count()

    open_alerts = db.query(Alert).filter(Alert.status == "OPEN").count()

    resolved_alerts = db.query(Alert).filter(Alert.status == "RESOLVED").count()

    high_risk_alerts = db.query(Alert).filter(Alert.risk_score >= 75).count()

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "resolved_alerts": resolved_alerts,
        "high_risk_alerts": high_risk_alerts,
    }