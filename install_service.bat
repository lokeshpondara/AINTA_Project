@echo off
echo Installing AINTA as Windows Service...
python windows_service.py install
echo Done. Check services.msc for 'AINTA_SOC'
echo Start: nssm start AINTA_SOC
pause
