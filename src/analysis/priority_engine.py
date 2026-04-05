def get_priority(alert):

    severity = alert.get("severity", 0)

    if severity >= 80:
        return "CRITICAL"
    elif severity >= 60:
        return "HIGH"
    elif severity >= 40:
        return "MEDIUM"
    else:
        return "Low"