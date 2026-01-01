@echo off
REM File Teleporter - Windows Setup Script
REM This script sets up the Python virtual environment and installs all dependencies

echo ========================================
echo File Teleporter - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Remove old virtual environment if it exists
if exist ".venv" (
    echo [2/4] Removing old virtual environment...
    rmdir /s /q .venv
    echo.
)

REM Create virtual environment
echo [2/4] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    echo.
    pause
    exit /b 1
)
echo Virtual environment created successfully.
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [4/4] Installing dependencies...
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing required packages (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    echo.
    pause
    exit /b 1
)
echo.

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo You can now run File Teleporter using:
echo   - Double-click: run_file_teleporter.bat
echo   - Or create a desktop shortcut to run_file_teleporter.bat
echo.
echo To build an executable (.exe), run:
echo   - build_exe.bat
echo.
pause
