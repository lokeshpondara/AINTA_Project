import os
import json
from datetime import datetime

EVIDENCE_DIR = "database/evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)


def save_evidence(data):

    filename = datetime.now().strftime("evidence_%Y%m%d_%H%M%S.json")
    filepath = os.path.join(EVIDENCE_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def save_alert(alert):

    save_evidence(alert, )