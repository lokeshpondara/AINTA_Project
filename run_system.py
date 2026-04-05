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

    time.sleep(3)

    start_dashboard()


if __name__ == "__main__":
    main()