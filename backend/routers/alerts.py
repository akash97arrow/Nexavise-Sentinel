from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Alert
from backend.schemas import AlertResponse, AlertUpdate
from backend.dependencies import get_current_user


router = APIRouter()


@router.get("/alerts", response_model=list[AlertResponse])
def get_alerts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).all()

    return alerts


@router.patch("/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    existing_alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if existing_alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    existing_alert.status = alert.status

    db.commit()
    db.refresh(existing_alert)

    return existing_alert