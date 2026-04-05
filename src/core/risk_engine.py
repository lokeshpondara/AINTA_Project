def calculate_risk(severity, abuse_score, events):

    risk = (
        severity * 0.5 +
        abuse_score * 0.3 +
        min(events * 2, 20)
    )

    if risk >= 80:
        return "CRITICAL", int(risk)
    elif risk >= 60:
        return "HIGH", int(risk)
    elif risk >= 40:
        return "MEDIUM", int(risk)
    else:
        return "LOW", int(risk)