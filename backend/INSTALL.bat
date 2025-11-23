@echo off
echo ================================================
echo AI Background Remover - ONE-CLICK INSTALLATION
echo ================================================
echo.
echo This will:
echo  1. Create Python virtual environment
echo  2. Install all dependencies
echo  3. Download Real-ESRGAN model
echo  4. Start the backend server
echo.
echo This will take 10-15 minutes on first run.
echo.
pause

cd /d "%~dp0backend"

REM Step 1: Create virtual environment
echo.
echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo Make sure Python 3.8+ is installed
    pause
    exit /b 1
)
echo [OK] Virtual environment created!

REM Step 2: Activate and upgrade pip
echo.
echo [2/4] Activating environment and upgrading pip...
call .\venv\Scripts\Activate
python -m pip install --upgrade pip
echo [OK] Pip upgraded!

REM Step 3: Install dependencies
echo.
echo [3/4] Installing Python packages (this takes 5-10 minutes)...
echo Please wait - downloading PyTorch, rembg, Real-ESRGAN...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] All packages installed!

REM Step 4: Download Real-ESRGAN model
echo.
echo [4/4] Downloading Real-ESRGAN model (67 MB)...
if not exist "models\" mkdir models
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth' -OutFile 'models\RealESRGAN_x2plus.pth'"
if exist "models\RealESRGAN_x2plus.pth" (
    echo [OK] Model downloaded!
) else (
    echo [WARNING] Model download failed. You can download manually from:
    echo https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth
    echo Save it to: backend\models\RealESRGAN_x2plus.pth
)

echo.
echo ================================================
echo INSTALLATION COMPLETE!
echo ================================================
echo.
echo Starting the backend server now...
echo.
python api.py

pause
