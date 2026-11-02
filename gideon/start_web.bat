@echo off
title Gideon Agentic OS - Web Dashboard
echo Starting Gideon Agentic OS Command Center on http://127.0.0.1:8080 ...
cd /d "%~dp0"
call ..\open-dots\server\.venv\Scripts\activate.bat
python run_gideon.py --web
pause
