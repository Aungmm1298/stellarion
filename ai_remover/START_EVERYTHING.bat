@echo off
echo ================================================
echo    AI Background Remover - Complete Startup
echo ================================================
echo.
echo Starting backend server...
echo.

cd backend
start "AI Background Remover Server" cmd /k "python api.py"

timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo Backend server is starting...
echo.
echo Wait 5-10 seconds for models to load, then:
echo 1. Open index.html in your browser
echo 2. Or visit: http://127.0.0.1:5500/index.html
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ================================================
echo.
echo Press any key to open the folder...
pause >nul

cd ..
explorer .

echo.
echo Backend is running in a separate window.
echo Close that window when you're done.
