from html import escape

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Asset, Scan, Finding, AttackPath
from backend.dependencies import get_current_user


router = APIRouter()


@router.get(
    "/reports/{asset_id}/download",
    response_class=HTMLResponse,
)
def download_asset_report(
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

    # Escape user/database-controlled values before inserting into HTML.
    asset_name = escape(str(asset.name))
    asset_target = escape(str(asset.target))
    asset_type = escape(str(asset.asset_type))
    authorization_status = escape(
        str(asset.authorization_status)
    )

    finding_rows = ""

    for finding in findings:
        finding_rows += f"""
        <tr>
            <td>{finding.id}</td>
            <td>{escape(str(finding.title))}</td>
            <td>{escape(str(finding.severity))}</td>
            <td>{finding.risk_score}</td>
            <td>{escape(str(finding.risk_level or "-"))}</td>
            <td>{escape(str(finding.status))}</td>
        </tr>
        """

    attack_rows = ""

    for path in attack_paths:
        attack_rows += f"""
        <tr>
            <td>{path.id}</td>
            <td>{path.finding_id}</td>
            <td>{escape(str(path.entry_point))}</td>
            <td>{path.risk_score}</td>
            <td>{escape(str(path.risk_level))}</td>
            <td>{escape(str(path.status))}</td>
        </tr>
        """

    if latest_scan:
        latest_scan_html = f"""
        <p>
            <strong>Scan ID:</strong> {latest_scan.id}<br>
            <strong>Status:</strong> {escape(str(latest_scan.status))}<br>
            <strong>Started:</strong> {escape(str(latest_scan.started_at))}<br>
            <strong>Completed:</strong> {escape(str(latest_scan.completed_at))}
        </p>
        """
    else:
        latest_scan_html = (
            "<p>No completed scan available.</p>"
        )

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nexavise Sentinel Security Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            color: #1f2937;
            background: #ffffff;
        }}

        h1 {{
            color: #111827;
        }}

        h2 {{
            margin-top: 35px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 8px;
        }}

        .header {{
            border-bottom: 3px solid #111827;
            padding-bottom: 20px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
        }}

        .card {{
            border: 1px solid #d1d5db;
            padding: 15px;
            border-radius: 8px;
        }}

        .number {{
            font-size: 28px;
            font-weight: bold;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            border: 1px solid #d1d5db;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #f3f4f6;
        }}

        .footer {{
            margin-top: 50px;
            padding-top: 15px;
            border-top: 1px solid #d1d5db;
            font-size: 12px;
            color: #6b7280;
        }}
    </style>
</head>

<body>

    <div class="header">
        <h1>Nexavise Sentinel Security Assessment Report</h1>

        <p>
            <strong>Asset:</strong> {asset_name}<br>
            <strong>Target:</strong> {asset_target}<br>
            <strong>Type:</strong> {asset_type}<br>
            <strong>Authorization:</strong> {authorization_status}
        </p>
    </div>

    <h2>Security Summary</h2>

    <div class="summary">

        <div class="card">
            <div>Total Scans</div>
            <div class="number">{scan_count}</div>
        </div>

        <div class="card">
            <div>Total Findings</div>
            <div class="number">{len(findings)}</div>
        </div>

        <div class="card">
            <div>Open Findings</div>
            <div class="number">{open_findings}</div>
        </div>

        <div class="card">
            <div>Critical Findings</div>
            <div class="number">{critical_findings}</div>
        </div>

    </div>

    <h2>Latest Scan</h2>

    {latest_scan_html}

    <h2>Findings</h2>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Finding</th>
                <th>Severity</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Status</th>
            </tr>
        </thead>

        <tbody>
            {finding_rows}
        </tbody>
    </table>

    <h2>Attack Paths</h2>

    <p>
        <strong>Total:</strong> {len(attack_paths)}
        &nbsp;&nbsp;
        <strong>Open:</strong> {open_attack_paths}
    </p>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Finding ID</th>
                <th>Entry Point</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Status</th>
            </tr>
        </thead>

        <tbody>
            {attack_rows}
        </tbody>
    </table>

    <div class="footer">
        Generated by Nexavise Sentinel
    </div>

</body>
</html>
"""

    return HTMLResponse(
        content=html,
        headers={
            "Content-Disposition":
                f'attachment; filename="nexavise-report-asset-{asset_id}.html"'
        },
    )