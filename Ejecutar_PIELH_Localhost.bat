@echo off
setlocal

title PIELH QA - Clean Restart

cd /d "%~dp0"

if not exist logs mkdir logs

echo Cerrando instancias anteriores...

REM Mata cualquier server.py previo
taskkill /F /IM python.exe >nul 2>&1

REM Libera puerto 8080 si queda bloqueado
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8080" ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 >nul

:restart

echo [%date% %time%] Iniciando servidor... >> logs\server_restart.log

python server.py

echo [%date% %time%] Servidor detenido. Reiniciando... >> logs\server_restart.log

echo Reiniciando en 5 segundos...
timeout /t 5 /nobreak >nul

goto restart