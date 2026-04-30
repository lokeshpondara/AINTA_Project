import os
import sys
import time
import threading
import subprocess

from src.storage.database_manager import init_db
from src.monitoring.monitor_engine import start_monitoring

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


# -----------------------------
# Reset previous outputs
# -----------------------------
def reset_outputs():

    files = [
        "OUTPUT/alerts.log",
        "OUTPUT/detection_results.csv",
        "database/alerts.db"
    ]

    for f in files:
        try:
            if os.path.exists(f):
                os.remove(f)
                print("Removed old file:", f)
        except PermissionError:
            print("File in use, skipping:", f)

    print("System reset complete\n")


# -----------------------------
# Start IDS engine
# -----------------------------
def start_ids():

    print("Starting AINTA IDS engine...\n")
    start_monitoring()


# -----------------------------
# Launch dashboard
# -----------------------------
def start_dashboard():

    print("Launching SOC dashboard...\n")

    dashboard_path = os.path.join(ROOT_DIR, "dashboard.py")
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        dashboard_path
    ], check=True)


# -----------------------------
# Main controller
# -----------------------------
def main():

    print("\n=============================")
    print("   AINTA SOC SYSTEM STARTING")
    print("=============================\n")

    reset_outputs()

    # IMPORTANT: recreate database table
    init_db()

    time.sleep(1)

    ids_thread = threading.Thread(target=start_ids)
    ids_thread.daemon = True
    ids_thread.start()

    def siem_export_loop():
        import time
        from src.storage.siem_exporter import export_siem_json
        while True:
            time.sleep(3600)
            export_siem_json()

    siem_thread = threading.Thread(target=siem_export_loop, daemon=True)
    siem_thread.start()

    time.sleep(3)

    start_dashboard()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", action="store_true", help="Run as service mode")
    args = parser.parse_args()
    
    if args.service:
        main()  # No dashboard for service
    else:
        main()
