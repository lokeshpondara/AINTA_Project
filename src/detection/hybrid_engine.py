import random

def hybrid_detect(flow, pred, port_tracker):

    try:
        src_ip = flow.get("src")
        dst_port = flow.get("dst_port")
        packet_rate = flow.get("packet_rate", 0)

        if not src_ip:
            return None

        # ---------------- TRACK PORTS ----------------
        if src_ip not in port_tracker:
            port_tracker[src_ip] = []

        port_tracker[src_ip].append(dst_port)

        if len(port_tracker[src_ip]) > 50:
            port_tracker[src_ip].pop(0)  # keep last 50 ports
        unique_ports = len(set(port_tracker[src_ip]))

        # ---------------- DEFAULT ----------------
        attack = "Normal"
        severity = 0
        reason = []

        # ---------------- RULES ----------------

        # Port Scan
        if unique_ports > 5:
            attack = "Port Scan"
            severity = 60
            reason.append("Multiple ports accessed")

        # DDoS
        if packet_rate > 50:
            attack = "DDoS"
            severity = 80
            reason.append("High traffic rate")

        # AI anomaly
        if pred == -1:
            attack = "Anomalous Traffic"
            severity = max(severity, 40)
            reason.append("AI anomaly detected")

        # Strong attack
        if pred == -1 and packet_rate > 100:
            attack = "DDoS"
            severity = 90
            reason.append("Severe anomaly spike")

        # ---------------- FINAL CHECK ----------------
        if severity == 0:
            return None

        # ---------------- RANDOMIZE (IMPORTANT) ----------------
        severity += random.randint(-5, 5)
        severity = max(10, min(severity, 100))

        return {
            "attack": attack,
            "severity": severity,
            "packet_rate": packet_rate,
            "reason": reason,
            "src_ip": src_ip
        }

    except Exception as e:
        print(f"[ERROR] Hybrid detection failed: {e}")
        return None