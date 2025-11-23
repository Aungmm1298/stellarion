@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete! 
echo.
echo To start the server:
echo 1. Activate the environment: venv\Scripts\activate
echo 2. Run the server: python main.py
echo.
pause
