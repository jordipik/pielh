@echo off
cd /d %~dp0
python -m pip install requests shapely
python scripts\download_hospitalet_streets.py
pause
