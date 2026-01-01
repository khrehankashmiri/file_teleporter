@echo off
REM File Teleporter Launcher for Windows
REM This script activates the virtual environment and runs the application

echo Starting File Teleporter...
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_windows.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    echo.
    pause
    exit /b 1
)

REM Run the application
python file_teleporter.py

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
