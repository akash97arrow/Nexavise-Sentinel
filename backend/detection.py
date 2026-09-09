def analyze_event(event_type: str, severity: str):
    if event_type == "BRUTE_FORCE":
        return {
            "threat": True,
            "risk_score": 90,
            "message": "Possible brute-force attack detected"
        }

    if event_type == "MALWARE_DETECTED":
        return {
            "threat": True,
            "risk_score": 100,
            "message": "Malware activity detected"
        }

    if severity.upper() == "HIGH":
        return {
            "threat": True,
            "risk_score": 75,
            "message": "High-severity security event detected"
        }

    if severity.upper() == "MEDIUM":
        return {
            "threat": True,
            "risk_score": 50,
            "message": "Medium-risk security event detected"
        }

    return {
        "threat": False,
        "risk_score": 10,
        "message": "Normal security event"
    }