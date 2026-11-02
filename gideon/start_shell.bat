@echo off
title Gideon Agentic OS - Terminal Shell
cd /d "%~dp0"
call ..\open-dots\server\.venv\Scripts\activate.bat
python run_gideon.py
pause
