from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    Asset,
    Scan,
    ScanResult,
    SecurityEvent,
    Alert,
    Finding,
    AttackPath,
)
from backend.dependencies import get_current_user

from backend.routers.users import router as users_router
from backend.routers.events import router as events_router
from backend.routers.alerts import router as alerts_router
from backend.routers.assets import router as assets_router
from backend.routers.scans import router as scans_router
from backend.routers.findings import router as findings_router
from backend.routers.finding_occurrences import router as finding_occurrences_router
from backend.routers.attack_paths import router as attack_paths_router
from backend.routers.reports import router as reports_router
from backend.routers.report_export import router as report_export_router

app = FastAPI(title="Nexavise Sentinel API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(events_router)
app.include_router(users_router)
app.include_router(alerts_router)
app.include_router(assets_router)
app.include_router(scans_router)
app.include_router(findings_router)
app.include_router(finding_occurrences_router)
app.include_router(attack_paths_router)
app.include_router(reports_router)
app.include_router(report_export_router)


@app.get("/db-test")
def database_test(
    db: Session = Depends(get_db),
):
    return {
        "status": "ok",
        "message": "SQLAlchemy database session is working",
    }


@app.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # User-owned assets
    user_asset_ids = db.query(Asset.id).filter(Asset.user_id == current_user).subquery()

    # Security Events
    total_events = (
        db.query(SecurityEvent).filter(SecurityEvent.user_id == current_user).count()
    )

    # Alerts
    total_alerts = db.query(Alert).filter(Alert.user_id == current_user).count()

    open_alerts = (
        db.query(Alert)
        .filter(
            Alert.user_id == current_user,
            Alert.status == "OPEN",
        )
        .count()
    )

    resolved_alerts = (
        db.query(Alert)
        .filter(
            Alert.user_id == current_user,
            Alert.status == "RESOLVED",
        )
        .count()
    )

    high_risk_alerts = (
        db.query(Alert)
        .filter(
            Alert.user_id == current_user,
            Alert.risk_score >= 75,
        )
        .count()
    )

    # Findings
    total_findings = (
        db.query(Finding).filter(Finding.asset_id.in_(user_asset_ids)).count()
    )

    open_findings = (
        db.query(Finding)
        .filter(
            Finding.asset_id.in_(user_asset_ids),
            Finding.status == "OPEN",
        )
        .count()
    )

    resolved_findings = (
        db.query(Finding)
        .filter(
            Finding.asset_id.in_(user_asset_ids),
            Finding.status == "RESOLVED",
        )
        .count()
    )

    critical_findings = (
        db.query(Finding)
        .filter(
            Finding.asset_id.in_(user_asset_ids),
            Finding.risk_score >= 75,
        )
        .count()
    )

    # Attack Paths
    total_attack_paths = (
        db.query(AttackPath).filter(AttackPath.asset_id.in_(user_asset_ids)).count()
    )

    open_attack_paths = (
        db.query(AttackPath)
        .filter(
            AttackPath.asset_id.in_(user_asset_ids),
            AttackPath.status == "OPEN",
        )
        .count()
    )

    resolved_attack_paths = (
        db.query(AttackPath)
        .filter(
            AttackPath.asset_id.in_(user_asset_ids),
            AttackPath.status == "RESOLVED",
        )
        .count()
    )

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "resolved_alerts": resolved_alerts,
        "high_risk_alerts": high_risk_alerts,
        "total_findings": total_findings,
        "open_findings": open_findings,
        "resolved_findings": resolved_findings,
        "critical_findings": critical_findings,
        "total_attack_paths": total_attack_paths,
        "open_attack_paths": open_attack_paths,
        "resolved_attack_paths": resolved_attack_paths,
    }
