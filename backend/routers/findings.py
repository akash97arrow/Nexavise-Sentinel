from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import (
    Asset,
    Finding,
    FindingOccurrence,
    Scan,
)
from backend.schemas import (
    FindingResponse,
    FindingUpdate,
    FindingOccurrenceResponse,
)
from backend.dependencies import get_current_user


router = APIRouter()


# GET /findings
@router.get(
    "/findings",
    response_model=list[FindingResponse],
)
def get_findings(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    findings = (
        db.query(Finding)
        .join(
            Asset,
            Finding.asset_id == Asset.id,
        )
        .filter(
            Asset.user_id == current_user
        )
        .order_by(
            Finding.created_at.desc()
        )
        .all()
    )

    return findings


# GET /findings/{finding_id}/occurrences
@router.get(
    "/findings/{finding_id}/occurrences",
    response_model=list[FindingOccurrenceResponse],
)
def get_finding_occurrences(
    finding_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    finding = (
        db.query(Finding)
        .join(
            Asset,
            Finding.asset_id == Asset.id,
        )
        .filter(
            Finding.id == finding_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if finding is None:
        raise HTTPException(
            status_code=404,
            detail="Finding not found",
        )

    occurrences = (
        db.query(FindingOccurrence)
        .filter(
            FindingOccurrence.finding_id == finding_id
        )
        .order_by(
            FindingOccurrence.created_at.desc()
        )
        .all()
    )

    return occurrences


# GET /findings/latest
@router.get(
    "/findings/latest",
    response_model=list[FindingResponse],
)
def get_latest_findings(
    asset_id: int = Query(
        ...,
        description="Asset ID to get latest findings for",
    ),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    asset = (
        db.query(Asset)
        .filter(
            Asset.id == asset_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    latest_scan = (
        db.query(Scan)
        .filter(
            Scan.asset_id == asset_id,
            Scan.status == "COMPLETED",
        )
        .order_by(
            Scan.id.desc()
        )
        .first()
    )

    if latest_scan is None:
        return []

    findings = (
        db.query(Finding)
        .join(
            FindingOccurrence,
            FindingOccurrence.finding_id == Finding.id,
        )
        .filter(
            FindingOccurrence.scan_id == latest_scan.id,
            Finding.asset_id == asset_id,
        )
        .order_by(
            Finding.created_at.desc()
        )
        .all()
    )

    response = []

    for finding in findings:

        occurrence_count = (
            db.query(
                func.count(FindingOccurrence.id)
            )
            .filter(
                FindingOccurrence.finding_id == finding.id
            )
            .scalar()
        )

        last_seen_scan_id = (
            db.query(
                func.max(FindingOccurrence.scan_id)
            )
            .filter(
                FindingOccurrence.finding_id == finding.id
            )
            .scalar()
        )

        response.append(
            {
                "id": finding.id,
                "asset_id": finding.asset_id,
                "scan_result_id": finding.scan_result_id,
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity,
                "risk_score": finding.risk_score,
                "risk_level": finding.risk_level,
                "status": finding.status,
                "created_at": finding.created_at,
                "last_seen_scan_id": last_seen_scan_id,
                "occurrence_count": occurrence_count or 0,
            }
        )

    return response


# PATCH /findings/{finding_id}
@router.patch(
    "/findings/{finding_id}",
    response_model=FindingResponse,
)
def update_finding(
    finding_id: int,
    finding: FindingUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    existing_finding = (
        db.query(Finding)
        .join(
            Asset,
            Finding.asset_id == Asset.id,
        )
        .filter(
            Finding.id == finding_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if existing_finding is None:
        raise HTTPException(
            status_code=404,
            detail="Finding not found",
        )

    status = finding.status.strip().upper()

    if status not in ("OPEN", "RESOLVED"):
        raise HTTPException(
            status_code=400,
            detail="Status must be OPEN or RESOLVED",
        )

    existing_finding.status = status

    db.commit()
    db.refresh(existing_finding)

    return existing_finding