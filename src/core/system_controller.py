class SystemController:

    def __init__(self):
        self.active_alerts = []

    def process_alert(self, alert):
        # Step 1: enrich
        alert = self.enrich(alert)

        # Step 2: score
        alert["threat_score"] = self.score(alert)

        # Step 3: prioritize
        alert["priority"] = self.prioritize(alert)

        # Step 4: store
        self.active_alerts.append(alert)

        return alert

    def enrich(self, alert):
        # integrate threat intel here
        return alert

    def score(self, alert):
        return int(alert["severity"] * 0.7)

    def prioritize(self, alert):
        if alert["threat_score"] > 80:
            return "CRITICAL"
        elif alert["threat_score"] > 60:
            return "HIGH"
        return "MEDIUM"