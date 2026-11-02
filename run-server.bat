@echo off
cd /d "%~dp0"
python server.py --host 0.0.0.0 --ports 8992-8995
pause
