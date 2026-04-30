import os
import sys
import time
import logging
import traceback


from src.processing.flow_extractor import extract_flow
from src.processing.feature_engineering import build_features

from src.detection.anomaly_detector import load_model, detect
from src.detection.threat_intel import check_ip

from src.response.windows_firewall import windows_block_ip as block_ip
from src.response.auto_response import respond
from src.response.ip_blacklist import is_blacklisted, add_to_blacklist

from src.storage.database_manager import insert_alert
from src.storage.evidence_writer import save_alert
from src.storage.report_writer import generate_report

from src.analysis.ip_geolocation import get_location
from src.analysis.incident_correlation import IncidentCorrelator

from src.detection.severity_engine import calculate_severity
from src.detection.mitre_mapping import map_mitre

from src.core.risk_engine import calculate_risk
from src.core.decision_engine import DecisionEngine
from src.core.system_controller import SystemController


# ---------------- PATH FIX ----------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def start_monitoring():

    model = load_model()
    controller = SystemController()
    correlator = IncidentCorrelator()
    decision_engine = DecisionEngine()

    if model is None:
        print("❌ Model not loaded")
        return

    packet_buffer = []
    last_seen = {}

    print("🚀 Monitoring started")

    while True:
        try:
            packet_buffer.clear()
            from src.capture.packet_capture import multi_continuous_capture
            multi_continuous_capture(packet_buffer)  # threads daemon, no need save

            if not packet_buffer:
                continue

            flows = {}

            for pkt in packet_buffer:
                flow = extract_flow(pkt)
                if not flow:
                    continue

                key = (
                    flow["src"],
                    flow["dst"],
                    flow["src_port"],
                    flow["dst_port"],
                    flow["protocol"]
                )

                flows[key] = flow

            if not flows:
                continue

            features = build_features(flows)
            if features.empty:
                continue

            predictions, scores = detect(model, features)
            
            # Phase 5 GNN (graceful fallback)
            try:
                import numpy as np
                from src.detection.gnn_detector import load_gnn_model, detect_gnn
                gnn_model, scaler = load_gnn_model()
                if gnn_model:
                    gnn_scores = detect_gnn(gnn_model, scaler, features)
                    scores = np.maximum(scores, np.array(gnn_scores))
            except ImportError:
                print("GNN fallback: using IsolationForest only")

            for flow, pred, score in zip(flows.values(), predictions, scores):

                src_ip = flow.get("src")
                packet_rate = flow.get("packet_rate", 0)

                if not src_ip or is_blacklisted(src_ip):
                    continue

# reduce noise
                # DEBUG disabled for clean terminal
                if pred == 1 and packet_rate < 10:  # lowered for more detections
                    continue

                # anti-spam
                now = time.time()
                if src_ip in last_seen and now - last_seen[src_ip] < 5:
                    continue
                last_seen[src_ip] = now

                # intel
                intel = check_ip(src_ip) or {}

                # severity
                severity = calculate_severity(
                    score,
                    packet_rate,
                    intel.get("confidence", 0)
                )

                # attack type
                if packet_rate > 1000:
                    attack = "DDoS"
                elif packet_rate > 200:
                    attack = "Traffic Flood"
                else:
                    attack = "Suspicious Activity"

                # geo
                geo = get_location(src_ip) or {}

                country = geo.get("country", "unknown")
                lat = geo.get("latitude", 0.0)
                lon = geo.get("longitude", 0.0)

                # alert object
                alert = controller.process_alert({
                    "timestamp": time.ctime(),
                    "src_ip": src_ip,
                    "attack": attack,
                    "packet_rate": packet_rate,
                    "severity": severity,
                    "confidence": intel.get("confidence", 0),
                    "country": country,
                    "epoch": time.time()
                })

                # ---------------- CORRELATION ----------------
                incident = correlator.correlate(alert)

                if not incident:
                    continue

                # ---------------- MITRE ----------------
                mitre = map_mitre(attack) or {}

                # ---------------- RISK ----------------
                priority, risk_score = calculate_risk(
                    severity,
                    intel.get("abuse_score", 0),
                    incident.get("events", 1)
                )

                alert.update({
                    "mitre_tactic": mitre.get("tactic", "unknown"),
                    "mitre_technique": mitre.get("technique", "unknown"),
                    "risk_score": risk_score,
                    "priority": priority
                })

                # ---------------- DECISION ----------------
                action = decision_engine.decide(incident)

                # ---------------- STORE ----------------
                # Full insert with all fields
                insert_alert(
                    alert["timestamp"],
                    alert["src_ip"],
                    alert["attack"],
                    alert["packet_rate"],
                    alert["severity"],
                    alert.get("confidence", 0),
                    country,
                    intel.get("isp", "unknown"),
                    lat,
                    lon,
                    alert.get("risk_score", 0),
                    alert.get("priority", "LOW"),
                    alert.get("mitre_tactic", "unknown"),
                    alert.get("mitre_technique", "unknown")
                )

                save_alert(alert)
                generate_report(src_ip, attack, severity)

                respond(alert)
                from src.response.email_alert import send_notification
                send_notification(alert)
                
                # SIEM export on high severity
                if severity >= 70:
                    from src.storage.siem_exporter import export_siem_json
                    export_siem_json(since_hours=1)

                # ---------------- RESPONSE ----------------
                print("\\n" + "="*80)
                print(f"🚨 THREAT: {src_ip} | {attack} | Sev={severity} | Risk={alert.get('risk_score',0)} | Events={incident.get('events',1)} | Action={action}")
                print("="*80)

                if action == "BLOCK":
                    print(f"🚫 BLOCKING {src_ip}")
                    block_ip(src_ip)
                    add_to_blacklist(src_ip)

                elif action == "MONITOR":
                    print(f"👁 MONITORING {src_ip}")

        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()
            time.sleep(3)


if __name__ == "__main__":
    start_monitoring()