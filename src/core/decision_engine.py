class DecisionEngine:

    def decide(self, incident):

        if not incident:
            return "IGNORE"

        sev = incident.get("max_severity", 0)
        events = incident.get("events", 0)

        if sev >=80:
            return "BLOCK"
        if sev >= 60:
            return "MONITOR"
        if events > 10:
            return "MONITOR"

        return "IGNORE"