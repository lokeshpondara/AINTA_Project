from src.response.firewall_blocker import block_ip
from src.storage.incident_report import generate_report

def respond(alert):

    severity = alert["severity"]
    ip = alert["src_ip"]

    if severity >= 80:
        print(f"CRITICAL threat from {ip} — blocking attacker")
        block_ip(ip)

    elif severity >= 50:
        print(f"High threat from {ip} — generating incident report")
        generate_report(ip, alert["attack"], severity)

    elif severity >= 20:
        print(f"Medium threat from {ip} — monitoring")

    else:
        print(f"Low threat from {ip} — logged only")