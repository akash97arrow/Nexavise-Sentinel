from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Asset, Scan, Finding, AttackPath
from backend.dependencies import get_current_user

router = APIRouter()


@router.get("/reports/{asset_id}")
def generate_asset_report(
    asset_id: int,
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
        .order_by(Scan.id.desc())
        .first()
    )

    findings = (
        db.query(Finding)
        .filter(Finding.asset_id == asset_id)
        .order_by(Finding.risk_score.desc())
        .all()
    )

    attack_paths = (
        db.query(AttackPath)
        .filter(AttackPath.asset_id == asset_id)
        .order_by(AttackPath.risk_score.desc())
        .all()
    )

    scan_count = (
        db.query(Scan)
        .filter(Scan.asset_id == asset_id)
        .count()
    )

    open_findings = sum(
        1 for finding in findings
        if finding.status == "OPEN"
    )

    critical_findings = sum(
        1 for finding in findings
        if finding.risk_score >= 75
    )

    open_attack_paths = sum(
        1 for path in attack_paths
        if path.status == "OPEN"
    )

    return {
        "report": {
            "title": "Nexavise Sentinel Security Assessment Report",
            "asset": {
                "id": asset.id,
                "name": asset.name,
                "target": asset.target,
                "type": asset.asset_type,
                "authorization_status": asset.authorization_status,
            },
            "summary": {
                "total_scans": scan_count,
                "total_findings": len(findings),
                "open_findings": open_findings,
                "critical_findings": critical_findings,
                "total_attack_paths": len(attack_paths),
                "open_attack_paths": open_attack_paths,
            },
            "latest_scan": (
                {
                    "id": latest_scan.id,
                    "status": latest_scan.status,
                    "started_at": latest_scan.started_at,
                    "completed_at": latest_scan.completed_at,
                }
                if latest_scan
                else None
            ),
            "findings": [
                {
                    "id": finding.id,
                    "title": finding.title,
                    "description": finding.description,
                    "severity": finding.severity,
                    "risk_score": finding.risk_score,
                    "risk_level": finding.risk_level,
                    "status": finding.status,
                }
                for finding in findings
            ],
            "attack_paths": [
                {
                    "id": path.id,
                    "finding_id": path.finding_id,
                    "entry_point": path.entry_point,
                    "risk_score": path.risk_score,
                    "risk_level": path.risk_level,
                    "status": path.status,
                }
                for path in attack_paths
            ],
        }
    }