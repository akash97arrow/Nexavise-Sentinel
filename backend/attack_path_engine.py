def generate_attack_path(finding, scan_result):
    """
    Generate an attack path from an exposed service finding.
    """

    if finding.status != "OPEN":
        return None

    if scan_result.state != "OPEN":
        return None

    if scan_result.port in (3306, 5432):
        entry_point = f"{scan_result.service} database"

    elif scan_result.port in (80, 443, 8000, 8080):
        entry_point = "Web service"

    elif scan_result.port == 22:
        entry_point = "SSH remote access"

    else:
        entry_point = f"{scan_result.service} service"

    return {
        "entry_point": entry_point,
        "risk_score": finding.risk_score,
        "risk_level": finding.risk_level,
    }