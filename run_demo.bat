@echo off
echo Starting AINTA demo...
start "Dummy" python attacks/dummy_server.py
timeout /t 2
start "DDoS" python attacks/ddos_simulator.py
start "PortScan" python attacks/port_scan_simulator.py
start "AINTA" python run_system.py
echo Open http://localhost:8501 for dashboard
echo Check terminal for DEBUG alerts
pause
