import os
from datetime import datetime

OUTPUT_DIR = "OUTPUT"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_report(ip, attack, severity):

    # sanitize IP for filename
    safe_ip = ip.replace(":", "_").replace(".", "_")

    report = f"""
========== INCIDENT REPORT ==========
Time: {datetime.now()}

Attacker IP : {ip}
Attack Type : {attack}
Severity    : {severity}

Actions Taken
--------------
• Alert generated
• Threat intelligence checked
• Evidence stored
• Firewall block triggered

=====================================
"""

    filename = f"incident_{safe_ip}.txt"

    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(report)