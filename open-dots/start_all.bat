@echo off
title Open Dots Full Suite Launcher (India Dropshipping)
echo ============================================================
echo   OPEN DOTS INDIA DROPSHIPPING MULTI-AGENT WORKSPACE
echo ============================================================
echo.
echo Launching Backend Server on http://127.0.0.1:8000 ...
start "Open Dots Backend" cmd /k "cd /d %~dp0\server && call .venv\Scripts\activate.bat && python run.py"

echo Launching Frontend Client on http://127.0.0.1:3000 ...
start "Open Dots Frontend" cmd /k "cd /d %~dp0\client && npm run dev"

echo.
echo Both services are starting in separate windows.
echo Frontend URL: http://127.0.0.1:3000
echo Backend API : http://127.0.0.1:8000/docs
echo Auth Token  : opendots-india-dropshipping-secret
echo.
echo Press any key to exit this launcher window (services will stay running).
pause > nul
