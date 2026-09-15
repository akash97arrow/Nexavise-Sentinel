SEVERITY_SCORES = {
    "LOW": 25,
    "MEDIUM": 50,
    "HIGH": 75,
    "CRITICAL": 100,
}


SERVICE_SENSITIVITY = {
    "MySQL": 90,
    "PostgreSQL": 90,
    "SSH": 70,
    "HTTP": 50,
    "HTTPS": 40,
    "FTP": 80,
    "SMTP": 60,
    "DNS": 40,
    "POP3": 60,
    "IMAP": 60,
    "Unknown": 50,
}


def get_service_sensitivity(service: str) -> int:
    return SERVICE_SENSITIVITY.get(service, 50)

def get_exposure_score(target: str) -> int:
    if target in ("127.0.0.1", "localhost", "::1"):
        return 20

    return 80

def calculate_risk(
    severity: str,
    exposure_score: int,
    sensitivity_score: int,
    configuration_score: int,
):
    severity = severity.upper()

    severity_score = SEVERITY_SCORES.get(severity, 0)

    final_score = (
        severity_score * 0.40
        + exposure_score * 0.30
        + sensitivity_score * 0.20
        + configuration_score * 0.10
    )

    final_score = round(final_score)

    if final_score >= 75:
        risk_level = "CRITICAL"
    elif final_score >= 50:
        risk_level = "HIGH"
    elif final_score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
    }

