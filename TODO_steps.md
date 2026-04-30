# Phase 3 Completion Steps
Breakdown of approved plan. Mark [x] as completed.

## 1. Multi-interface async capture
- [x] Edit src/capture/packet_capture.py: Added multi_continuous_capture() using config.interfaces
- [x] Update src/monitoring/monitor_engine.py: Use multi_continuous_capture()


## 2. Email/Slack alerts
- [x] Enhance src/response/email_alert.py: Added send_notification(alert) with config SMTP/Slack
- [x] Edit src/monitoring/monitor_engine.py: Call send_notification after respond
- [x] Update config.yaml: Added email/slack configs

## 3. SIEM JSON export
- [x] Create src/storage/siem_exporter.py: export_siem_json() with geo/MITRE/priority to OUTPUT/siem_export_*.json
- [x] Edit src/monitoring/monitor_engine.py: Export on severity >=70
- [x] Edit run_system.py: Added periodic export thread (hourly)

## 4. Windows Firewall
- [x] Create src/response/windows_firewall.py: netsh advfirewall block/unblock with timed rules
- [x] Edit src/monitoring/monitor_engine.py: Import windows_block_ip as block_ip

## 5. Windows Service
- [x] Create windows_service.py: NSSM service installer/remover/status
- [x] Create install_service.bat: Run python windows_service.py install
- [x] Update run_system.py: Added --service flag (no dashboard)

## Followup
- [x] pip install pywin32 requests pyyaml
- [x] Test: run_system.py + attacks/ddos_simulator.py (successful: multi-capture active, DDoS detections sev=65 MONITOR, dashboard at localhost:8501, alerts logged)
- [x] Update original TODO.md with [x]
- [ ] attempt_completion
