@echo off
setlocal

title PIELH QA - Auto Restart

cd /d "%~dp0"

if not exist logs mkdir logs

:restart

echo [%date% %time%] Iniciando servidor... >> logs\server_restart.log
echo.
echo ==========================================
echo Iniciando PIELH QA...
echo ==========================================
echo.

python server.py

echo [%date% %time%] Servidor detenido. Reiniciando... >> logs\server_restart.log

echo.
echo ==========================================
echo El servidor se ha detenido.
echo Reiniciando en 5 segundos...
echo ==========================================
echo.

timeout /t 5 /nobreak >nul

goto restart