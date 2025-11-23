@echo off
COLOR 0A
title AI Background Remover - Startup Guide

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                                                               ║
echo  ║         🎨 AI Background Remover - Startup Guide 🎨          ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  ⚠️  IMPORTANT: The backend server must run FIRST!
echo.
echo  ══════════════════════════════════════════════════════════════
echo  📋 STARTUP STEPS:
echo  ══════════════════════════════════════════════════════════════
echo.
echo  Step 1: Press any key to START THE BACKEND SERVER
echo           (A new window will open - keep it open!)
echo.
pause

echo.
echo  ⏳ Starting backend server...
echo.

cd backend
start "🚀 AI Backend Server - DO NOT CLOSE THIS WINDOW" cmd /k "echo ══════════════════════════════════════════════════ & echo    AI Background Remover Backend Server & echo ══════════════════════════════════════════════════ & echo. & echo Starting Python server with AI models... & echo. & python api.py"

echo  ✓ Backend server is starting in a separate window
echo.
echo  ⏰ Waiting 8 seconds for models to load...
timeout /t 8 /nobreak >nul

echo.
echo  ══════════════════════════════════════════════════════════════
echo  📋 Step 2: Check Backend Status
echo  ══════════════════════════════════════════════════════════════
echo.
echo  Opening backend status page in your browser...
echo.

start http://localhost:8000/api/status

timeout /t 2 /nobreak >nul

echo  ✓ If you see JSON data, the backend is running!
echo  ✗ If you see "can't reach this page", wait a bit longer
echo.
echo  ══════════════════════════════════════════════════════════════
echo  📋 Step 3: Open the Application
echo  ══════════════════════════════════════════════════════════════
echo.
echo  Choose one option:
echo.
echo  [1] Open index.html with default browser
echo  [2] Open project folder (manually open index.html)
echo  [3] Show me the URLs I need
echo  [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Opening index.html...
    cd ..
    start index.html
    echo.
    echo ✓ Application opened!
    echo.
    echo 💡 If you see "Cannot connect to backend":
    echo    1. Wait a few more seconds for models to load
    echo    2. Refresh the page (F5)
    echo    3. Check the backend window is still open
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Opening project folder...
    cd ..
    explorer .
    echo.
    echo ✓ Folder opened!
    echo.
    echo 👉 Now open 'index.html' in your browser
    goto end
)

if "%choice%"=="3" (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo 📌 IMPORTANT URLS:
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo Backend API Status:
    echo   http://localhost:8000/api/status
    echo.
    echo Backend API Documentation:
    echo   http://localhost:8000/docs
    echo.
    echo Frontend Application:
    echo   Open 'index.html' in your browser
    echo   Or use VS Code Live Server
    echo.
    echo ══════════════════════════════════════════════════════════════
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Exiting... The backend server will keep running.
    echo Close the backend window when you're done.
    goto realend
)

:end
echo.
echo ══════════════════════════════════════════════════════════════
echo ✅ SETUP COMPLETE!
echo ══════════════════════════════════════════════════════════════
echo.
echo 📝 REMEMBER:
echo   • Keep the backend window open while using the app
echo   • Close it when you're done (CTRL+C or close window)
echo   • If you see connection errors, check the backend window
echo.
echo 🔗 Quick Links:
echo   Backend Status: http://localhost:8000/api/status
echo   API Docs: http://localhost:8000/docs
echo.
echo 💡 TIP: Bookmark this startup script for easy access!
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo Press any key to exit...
pause >nul

:realend
