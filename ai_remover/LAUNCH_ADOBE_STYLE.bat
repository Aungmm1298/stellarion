@echo off
color 0B
title Adobe-Style Background Remover - Hylife
cls

echo.
echo ========================================================
echo          ADOBE-STYLE BACKGROUND REMOVER
echo                    Hylife
echo ========================================================
echo.
echo  Your background remover now works EXACTLY like Adobe!
echo.
echo ========================================================
echo.

echo [STEP 1] Starting Backend Server...
echo.
cd backend
if not exist "START.bat" (
    echo ERROR: backend/START.bat not found!
    echo Please make sure you're in the correct directory.
    pause
    exit /b 1
)

echo Starting FastAPI server with AI models...
echo.
start "Backend Server" cmd /k "START.bat"

echo [Waiting for backend to initialize... 10 seconds]
timeout /t 10 /nobreak > nul

echo.
echo ========================================================
echo [STEP 2] Opening Adobe-Style Interface...
echo ========================================================
echo.

cd ..
if exist "index.html" (
    echo Opening in your default browser...
    start "" "index.html"
    echo.
    echo ========================================================
    echo.
    echo   READY! Your Adobe-style tool is now open!
    echo.
    echo   WORKFLOW:
    echo   1. Upload an image (drag or click)
    echo   2. AI processes automatically (2-5 seconds)
    echo   3. Compare with before/after slider
    echo   4. Choose background color (sidebar)
    echo   5. Download PNG result
    echo.
    echo   FEATURES:
    echo   - Adobe blue design
    echo   - Automatic processing
    echo   - Interactive comparison slider
    echo   - Professional edge refinement
    echo   - Custom backgrounds
    echo   - Quality enhancement (2x)
    echo.
    echo   KEYBOARD SHORTCUTS:
    echo   - ESC: Back to upload
    echo   - C: Toggle comparison
    echo   - D: Download image
    echo.
    echo ========================================================
    echo.
    echo   Backend is running in the other window.
    echo   Keep that window open while using the tool!
    echo.
    echo   To stop: Close the backend window or press Ctrl+C
    echo.
) else (
    echo ERROR: index.html not found!
    pause
    exit /b 1
)

echo Press any key to see documentation...
pause > nul

echo.
echo Opening quick reference guide...
if exist "START_HERE.md" (
    start "" "START_HERE.md"
) else (
    echo Quick reference not found. Check ADOBE_STYLE_GUIDE.md
)

echo.
echo ========================================================
echo  Background Remover is running!
echo  Keep this window open.
echo ========================================================
echo.

pause
