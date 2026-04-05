MITRE_MAP = {
    "DDoS": {
        "tactic": "Impact",
        "technique": "T1499 - Endpoint Denial of Service"
    },
    "Traffic Flood": {
        "tactic": "Impact",
        "technique": "T1498 - Network DoS"
    },
    "Suspicious Activity": {
        "tactic": "Reconnaissance",
        "technique": "T1046 - Network Service Scanning"
    }
}

def map_mitre(attack):
    return MITRE_MAP.get(attack, {
        "tactic": "Unknown",
        "technique": "Unknown"
    })