from backend.risk_engine import (
    calculate_risk,
    get_service_sensitivity,
    get_exposure_score,
)


def generate_finding(scan_result, target):
    if scan_result.state != "OPEN":
        return None

    # MySQL
    if scan_result.port == 3306:
        risk = calculate_risk(
            severity="HIGH",
            exposure_score=get_exposure_score(target),
            sensitivity_score=get_service_sensitivity(scan_result.service),
            configuration_score=60,
        )

        return {
            "title": "Exposed MySQL Service",
            "description": (
                "MySQL is accessible through an open TCP port. "
                "An exposed database service may increase the attack surface "
                "if it is not properly secured."
            ),
            "severity": "HIGH",
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
        }

    # PostgreSQL
    if scan_result.port == 5432:
        risk = calculate_risk(
            severity="HIGH",
            exposure_score=get_exposure_score(target),
            sensitivity_score=get_service_sensitivity(scan_result.service),
            configuration_score=60,
        )

        return {
            "title": "Exposed PostgreSQL Service",
            "description": (
                "PostgreSQL is accessible through an open TCP port. "
                "An exposed database service may increase the attack surface "
                "if it is not properly secured."
            ),
            "severity": "HIGH",
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
        }

    # HTTP / HTTPS
    if scan_result.port in (80, 443, 8000, 8080):
        risk = calculate_risk(
            severity="MEDIUM",
            exposure_score=get_exposure_score(target),
            sensitivity_score=get_service_sensitivity(scan_result.service),
            configuration_score=60,
        )

        return {
            "title": "Exposed HTTP Service",
            "description": (
                "An HTTP service is accessible through an open TCP port. "
                "The service should be reviewed for secure configuration "
                "and unnecessary exposure."
            ),
            "severity": "MEDIUM",
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
        }

    # SSH
    if scan_result.port == 22:
        risk = calculate_risk(
            severity="MEDIUM",
            exposure_score=get_exposure_score(target),
            sensitivity_score=get_service_sensitivity(scan_result.service),
            configuration_score=60,
        )

        return {
            "title": "Exposed SSH Service",
            "description": (
                "SSH is accessible through an open TCP port. "
                "SSH should be protected with strong authentication "
                "and appropriate network restrictions."
            ),
            "severity": "MEDIUM",
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
        }

    # Generic open service
    risk = calculate_risk(
        severity="LOW",
        exposure_score=get_exposure_score(target),
        sensitivity_score=get_service_sensitivity(scan_result.service),
        configuration_score=60,
    )

    return {
        "title": f"Open {scan_result.service} Service",
        "description": (
            f"The {scan_result.service} service is accessible through "
            f"TCP port {scan_result.port}."
        ),
        "severity": "LOW",
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
    }