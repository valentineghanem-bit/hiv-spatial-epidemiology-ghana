@echo off
REM Windows launcher for HIV Spatial Epidemiology Dashboard

cd /d "%~dp0"

set DASHBOARD_URL=http://127.0.0.1:8050

echo Starting HIV Spatial Epidemiology Dashboard...
echo Opening browser at %DASHBOARD_URL%

REM Open URL in default browser
start "" "%DASHBOARD_URL%"

REM Wait a moment for browser to start
timeout /t 2 /nobreak

REM Start the Dash app
python app.py
pause
