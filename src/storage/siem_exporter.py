import json
import sqlite3
import os
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(ROOT_DIR, "database/alerts.db")
OUTPUT_DIR = os.path.join(ROOT_DIR, "OUTPUT")

def export_siem_json(since_hours=24):
    """Export alerts to SIEM JSON (Phase 3) - RFC5424-ish with extensions"""
    since = datetime.now().timestamp() - (since_hours * 3600)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, src_ip, attack_type, packet_rate, severity,
               confidence, country, isp, latitude, longitude, risk_score,
               priority, mitre_tactic, mitre_technique
        FROM alerts WHERE timestamp > ? ORDER BY id DESC
    """, (datetime.fromtimestamp(since).strftime('%Y-%m-%d %H:%M:%S'),))
    
    rows = cursor.fetchall()
    conn.close()
    
    events = []
    for row in rows:
        events.append({
            "@timestamp": row[0],
            "src_ip": row[1],
            "event_type": row[2],
            "packet_rate": row[3],
            "severity": row[4],
            "confidence": row[5],
            "geo": {
                "country": row[6],
                "isp": row[7],
                "location": [row[9], row[8]]  # lon, lat
            },
            "risk_score": row[10],
            "priority": row[11],
            "mitre": {
                "tactic": row[12],
                "technique": row[13]
            },
            "host": "ainta-soc"
        })
    
    siem_file = os.path.join(OUTPUT_DIR, f"siem_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(siem_file, 'w') as f:
        json.dump(events, f, indent=2)
    
    print(f"📊 SIEM export: {len(events)} events to {siem_file}")
    return siem_file
