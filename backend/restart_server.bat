@echo off
echo Restarting AI Background Remover Server...
echo.

REM Kill existing Python processes running the server
taskkill /F /IM python.exe /FI "WINDOWTITLE eq main_simple.py" 2>nul

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start the server
cd /d "%~dp0"
start /B python main_simple.py

echo.
echo Server started!
echo Backend running at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
