from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    Asset,
    Scan,
    ScanResult,
    Finding,
    FindingOccurrence,
    AttackPath,
)
from backend.dependencies import get_current_user
from backend.scanner import scan_port, validate_target
from backend.finding_engine import generate_finding
from backend.attack_path_engine import generate_attack_path
from backend.schemas import ScanResponse, ScanResultResponse


router = APIRouter()


COMMON_SCAN_PORTS = [
    21,
    22,
    25,
    53,
    80,
    110,
    143,
    443,
    3306,
    5432,
    8000,
    8080,
]


SCAN_COOLDOWN_SECONDS = 60


@router.post("/scans/{asset_id}")
def scan_asset(
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

    if asset.authorization_status.upper() != "AUTHORIZED":
        raise HTTPException(
            status_code=403,
            detail="Asset is not authorized for scanning",
        )

    if not validate_target(asset.target):
        raise HTTPException(
            status_code=400,
            detail="Invalid scan target",
        )

    # Prevent repeated scans on the same asset within 60 seconds.
    latest_scan = (
        db.query(Scan)
        .filter(Scan.asset_id == asset.id)
        .order_by(Scan.id.desc())
        .first()
    )

    if latest_scan is not None:
        scan_time = latest_scan.started_at

        if scan_time is not None:
            cooldown_until = scan_time + timedelta(
                seconds=SCAN_COOLDOWN_SECONDS
            )

            if datetime.utcnow() < cooldown_until:
                remaining_seconds = int(
                    (cooldown_until - datetime.utcnow()).total_seconds()
                )

                raise HTTPException(
                    status_code=429,
                    detail=(
                        f"Scan cooldown active. "
                        f"Please wait approximately "
                        f"{max(remaining_seconds, 1)} seconds."
                    ),
                )

    new_scan = Scan(
        asset_id=asset.id,
        status="RUNNING",
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    results = []

    try:
        for port in COMMON_SCAN_PORTS:
            result = scan_port(
                asset.target,
                port,
            )

            scan_result = ScanResult(
                asset_id=asset.id,
                scan_id=new_scan.id,
                port=result["port"],
                protocol=result["protocol"],
                service=result["service"],
                state=result["state"],
            )

            db.add(scan_result)
            db.flush()

            finding = generate_finding(
                scan_result,
                asset.target,
            )

            if finding:
                existing_finding = (
                    db.query(Finding)
                    .filter(
                        Finding.asset_id == asset.id,
                        Finding.title == finding["title"],
                    )
                    .first()
                )

                if existing_finding is None:
                    new_finding = Finding(
                        asset_id=asset.id,
                        scan_result_id=scan_result.id,
                        title=finding["title"],
                        description=finding["description"],
                        severity=finding["severity"],
                        risk_score=finding["risk_score"],
                        risk_level=finding.get("risk_level"),
                    )

                    db.add(new_finding)
                    db.flush()

                    finding_id = new_finding.id
                    current_finding = new_finding

                else:
                    existing_finding.risk_score = finding["risk_score"]
                    existing_finding.risk_level = finding.get("risk_level")

                    if existing_finding.status == "RESOLVED":
                        existing_finding.status = "OPEN"

                    finding_id = existing_finding.id
                    current_finding = existing_finding

                occurrence = FindingOccurrence(
                    finding_id=finding_id,
                    scan_id=new_scan.id,
                    scan_result_id=scan_result.id,
                )

                db.add(occurrence)

                attack_path = generate_attack_path(
                    current_finding,
                    scan_result,
                )

                if attack_path:
                    existing_attack_path = (
                        db.query(AttackPath)
                        .filter(
                            AttackPath.asset_id == asset.id,
                            AttackPath.finding_id == finding_id,
                        )
                        .first()
                    )

                    if existing_attack_path is None:
                        new_attack_path = AttackPath(
                            asset_id=asset.id,
                            finding_id=finding_id,
                            entry_point=attack_path["entry_point"],
                            risk_score=attack_path["risk_score"],
                            risk_level=attack_path["risk_level"],
                            status="OPEN",
                        )

                        db.add(new_attack_path)

                    else:
                        existing_attack_path.entry_point = (
                            attack_path["entry_point"]
                        )
                        existing_attack_path.risk_score = (
                            attack_path["risk_score"]
                        )
                        existing_attack_path.risk_level = (
                            attack_path["risk_level"]
                        )
                        existing_attack_path.status = "OPEN"

            results.append(result)

        new_scan.status = "COMPLETED"
        new_scan.completed_at = datetime.utcnow()

        db.commit()

    except Exception:
        new_scan.status = "FAILED"
        new_scan.completed_at = datetime.utcnow()
        db.commit()

        raise HTTPException(
            status_code=500,
            detail="Scan failed unexpectedly",
        )

    return {
        "scan_id": new_scan.id,
        "asset_id": asset.id,
        "target": asset.target,
        "status": new_scan.status,
        "results": results,
    }


@router.get(
    "/scans",
    response_model=list[ScanResponse],
)
def get_scans(
    asset_id: int | None = Query(
        None,
        description="Optional Asset ID to filter scan history",
    ),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    query = (
        db.query(Scan)
        .join(
            Asset,
            Scan.asset_id == Asset.id,
        )
        .filter(
            Asset.user_id == current_user,
        )
    )

    if asset_id is not None:
        query = query.filter(
            Scan.asset_id == asset_id
        )

    scans = (
        query
        .order_by(Scan.started_at.desc())
        .all()
    )

    return scans


@router.get(
    "/scans/{scan_id}/results",
    response_model=list[ScanResultResponse],
)
def get_scan_results(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    scan = (
        db.query(Scan)
        .join(
            Asset,
            Scan.asset_id == Asset.id,
        )
        .filter(
            Scan.id == scan_id,
            Asset.user_id == current_user,
        )
        .first()
    )

    if scan is None:
        raise HTTPException(
            status_code=404,
            detail="Scan not found",
        )

    results = (
        db.query(ScanResult)
        .filter(
            ScanResult.scan_id == scan_id
        )
        .order_by(
            ScanResult.port.asc()
        )
        .all()
    )

    return results


@router.get(
    "/scan-results",
    response_model=list[ScanResultResponse],
)
def get_all_scan_results(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    scan_results = (
        db.query(ScanResult)
        .join(
            Asset,
            ScanResult.asset_id == Asset.id,
        )
        .filter(
            Asset.user_id == current_user,
        )
        .order_by(
            ScanResult.created_at.desc()
        )
        .all()
    )

    return scan_results


@router.get(
    "/scan-results/latest",
    response_model=list[ScanResultResponse],
)
def get_latest_scan_results(
    asset_id: int = Query(
        ...,
        description="Asset ID to get latest scan results for",
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

    scan_results = (
        db.query(ScanResult)
        .filter(
            ScanResult.scan_id == latest_scan.id,
            ScanResult.asset_id == asset_id,
        )
        .order_by(
            ScanResult.created_at.desc()
        )
        .all()
    )

    return scan_results