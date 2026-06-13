@echo off
cd /d %~dp0

echo Iniciando PIELH QA...
start "" cmd /c "python server.py"

echo.
echo Servidor iniciado en http://localhost:8080
echo.
exit
