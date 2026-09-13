from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import SecurityEvent, Alert
from backend.schemas import SecurityEventCreate, SecurityEventResponse
from backend.dependencies import get_current_user
from backend.detection import analyze_event


router = APIRouter()


# POST /events
# Create a security event

@router.post("/events")
def create_event(
    event: SecurityEventCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_event = SecurityEvent(
        event_type=event.event_type,
        source_ip=event.source_ip,
        description=event.description,
        severity=event.severity
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    analysis = analyze_event(
        event.event_type,
        event.severity
    )

    if analysis["threat"]:
        new_alert = Alert(
            event_id=new_event.id,
            risk_score=analysis["risk_score"],
            message=analysis["message"]
        )

        db.add(new_alert)
        db.commit()

    return {
        "event": {
            "id": new_event.id,
            "event_type": new_event.event_type,
            "source_ip": new_event.source_ip,
            "description": new_event.description,
            "severity": new_event.severity,
            "created_at": new_event.created_at
        },
        "analysis": analysis
    }


# GET /events
# View security events

@router.get("/events", response_model=list[SecurityEventResponse])
def get_events(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    events = db.query(SecurityEvent).order_by(
        SecurityEvent.created_at.desc()
    ).all()

    return events