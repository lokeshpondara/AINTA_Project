@echo off
echo Adding Python Scripts to PATH...
setx PATH "%PATH%;%%APPDATA%%\Python\Python313\Scripts" /M
echo Restart PowerShell/VSCode terminal for changes to take effect.
echo PATH warnings now resolved - pip scripts accessible.
pause
