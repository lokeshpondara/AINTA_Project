import time
from collections import defaultdict

class IncidentCorrelator:

    def __init__(self):
        self.memory = defaultdict(list)

    def correlate(self, alert):

        src_ip = alert.get("src_ip")
        if not src_ip:
            return None

        now = time.time()

        # ✅ FIX: ensure epoch exists
        alert["epoch"] = now

        # store alert
        self.memory[src_ip].append(alert)

        # keep last 120 seconds only
        self.memory[src_ip] = [
            a for a in self.memory[src_ip]
            if now - a.get("epoch", now) < 120
        ]

        events = self.memory[src_ip]

        if not events:
            return None

        incident = {
            "src_ip": src_ip,
            "events": len(events),
            "max_severity": max([a.get("severity", 0) for a in events]),
            "total_packet_rate": sum([a.get("packet_rate", 0) for a in events]),
            "attacks": list(set([a.get("attack", "unknown") for a in events]))
        }

        return incident