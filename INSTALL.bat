@echo off
echo ========================================
echo AI Background Remover - Installation
echo ========================================
echo.

cd /d "%~dp0\backend"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
echo This may take 5-10 minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run backend\START.bat to start the server
echo 2. Open index.html in your browser
echo.
pause
