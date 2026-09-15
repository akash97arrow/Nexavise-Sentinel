from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import FindingOccurrence
from backend.schemas import FindingOccurrenceResponse
from backend.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/finding-occurrences",
    response_model=list[FindingOccurrenceResponse]
)
def get_finding_occurrences(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    occurrences = (
        db.query(FindingOccurrence)
        .order_by(FindingOccurrence.created_at.desc())
        .all()
    )

    return occurrences