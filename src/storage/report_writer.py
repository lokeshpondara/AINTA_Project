import os
import json
from datetime import datetime

OUTPUT_DIR = "OUTPUT"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_ALERTS = 1000


def save_alert(alert):
    filename = datetime.now().strftime("alerts_%Y%m%d.json")
    filepath = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load JSON: {e}")
            data = []
    else:
        data = []

    data.append(alert)

    if len(data) > MAX_ALERTS:
        data = data[-MAX_ALERTS:]

    temp_path = filepath + ".tmp"

    try:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=4)
        os.replace(temp_path, filepath)
    except Exception as e:
        print(f"[ERROR] Failed to save alert: {e}")

def generate_report(src_ip, attack, severity):
    from datetime import datetime
    import os

    OUTPUT_DIR = "OUTPUT"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 🔥 sanitize IP (IMPORTANT)
    safe_ip = src_ip.replace(":", "_").replace(".", "_")

    filename = f"report_{safe_ip}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(filepath, "a") as f:
            f.write("\n===== INCIDENT REPORT =====\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Source IP: {src_ip}\n")
            f.write(f"Attack Type: {attack}\n")
            f.write(f"Severity: {severity}\n")
            f.write("===========================\n")

    except Exception as e:
        print("[ERROR] Report write failed:", e)