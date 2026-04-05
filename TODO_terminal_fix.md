# Terminal Fix Plan Steps
Progress [ ]. Complete step-by-step.

1. Install missing deps
- [x] pip install flower flower-superlink[simulation]

2. Init DB
- [x] Run: python -c \"from src.storage.database_manager import init_db; init_db()\"

3. Lower detection thresholds & add logging
- [x] Edit src/monitoring/monitor_engine.py

## 4. Fix Flower server
- [ ] Edit src/federated/server.py OR use CLI

## 5. Test with attacks
- [ ] python attacks/ddos_simulator.py &
  python attacks/port_scan_simulator.py

## 6. Verify alerts
- [ ] python -c \"import sqlite3; print(sqlite3.connect('database/alerts.db').execute('SELECT COUNT(*) FROM alerts').fetchone()[0])\"
- [ ] python dashboard.py

## 7. Start federated
- [ ] flower-superlink --insecure
- [ ] Multi: python src/federated/client.py (2+ terminals)

## 8. Update TODOs [x]
- [ ] Mark Phase 5 complete

