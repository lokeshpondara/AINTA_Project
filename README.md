# AINTA – AI Enhanced Network Threat Analyzer

AINTA is an AI-based network monitoring system that detects anomalous traffic patterns using machine learning and visualizes threats through an interactive SOC-style dashboard.

## Features

• Packet capture using Scapy  
• Feature extraction from network flows  
• Isolation Forest anomaly detection  
• Rule-based attack classification  
• Evidence hashing for forensic validation  
• Real-time monitoring dashboard  
• Traffic analytics and visualization  

## Technologies

Python  
Scapy  
Scikit-learn  
Streamlit  
Matplotlib  
Pandas, NumPy, Plotly, PyDeck  

## Running the System

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the system:

```bash
python run_system.py
```

## Project Structure

```
AINTA_Project/
├── run_system.py          # Main system runner
├── dashboard.py           # Streamlit SOC dashboard
├── train_model.py         # ML model training
├── config.py              # Configuration
├── blacklist.txt          # Blocked IPs/hosts
├── requirements.txt       # Dependencies
├── attacks/               # Threat simulators (DDoS, Port Scan, Slowloris)
├── config/                # Config files
├── dashboard/             # Dashboard assets
├── DATA/                  # Datasets (CICIDS2017 sample, GeoIP DB)
├── database/              # SQLite alerts.db
├── evidence/              # Captured PCAP files (.pcap)
├── models/                # Trained anomaly_model.pkl
├── OUTPUT/                # Alerts JSON, incident reports
└── src/                   # Source code
```

## Quick Usage Examples

1. **Train anomaly detection model:**
   ```bash
   python train_model.py
   ```

2. **Run threat detection system:**
   ```bash
   python run_system.py
   ```

3. **Simulate attacks for testing:**
   ```bash
   cd attacks
   python ddos_simulator.py
   python port_scan_simulator.py
   python slowloris_simulator.py
   ```

4. **View dashboard** (opens automatically or via `streamlit run dashboard.py`)

## Detected Threats

AINTA detects and classifies:
- DDoS attacks
- Port scans
- Slowloris DoS
- Anomalous flows (Isolation Forest)
- Known bad IPs (blacklist.txt)

**Sample incidents logged in OUTPUT/:**
- 100+ incident reports (e.g., incident_20_42_65_84.txt)
- Port scans from 13.69.x.x ranges
- DDoS from AWS ranges (18.x.x.x, 20.x.x.x)
- Suspicious IPv6 attempts

## Outputs Generated

- `OUTPUT/alerts_YYYYMMDD.json`: JSON alert logs
- `OUTPUT/incident_IP.txt`: Detailed incident forensics
- `OUTPUT/evidence_hash.txt`: SHA hashes for validation
- `evidence/*.pcap`: Packet captures
- `database/alerts.db`: Persistent alert storage
- `system.log`: Runtime logs

## Evidence Validation

All detections include:
1. PCAP evidence files
2. Cryptographic hashes
3. Flow statistics
4. ML anomaly scores
5. Rule matches

## Development

1. Install dependencies
2. Train model with CICIDS2017 dataset
3. Run simulators for testing
4. Monitor dashboard for real-time alerts
