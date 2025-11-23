@echo off
echo =====================================
echo AI Background Remover - Quick Start
echo =====================================
echo.

cd /d "%~dp0backend"

REM Check if venv exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run the following commands first:
    echo.
    echo   cd backend
    echo   python -m venv venv
    echo   .\venv\Scripts\Activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and start server
echo [1/2] Starting Python Backend (FastAPI)...
echo.
start "AI Background Remover Backend" cmd /k "cd /d "%~dp0backend" && .\venv\Scripts\Activate && python api.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

echo.
echo [2/2] Opening Frontend...
echo.

REM Open index.html with default browser
start "" "%~dp0index.html"

echo.
echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: file:///%~dp0index.html
echo.
echo NOTE: If frontend shows connection error,
echo       open it with Live Server in VS Code
echo.
echo Press any key to exit (backend will keep running)...
pause >nul
