@echo off
title Open Dots Backend (India Dropshipping)
echo Starting Open Dots FastAPI Backend on http://127.0.0.1:8000...
cd /d "%~dp0\server"
call .venv\Scripts\activate.bat
python run.py
pause
