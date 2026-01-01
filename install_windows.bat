@echo off
REM Quick installer - Downloads and sets up File Teleporter

echo ========================================
echo File Teleporter - Quick Installer
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Opening download page...
    start https://www.python.org/downloads/
    echo.
    echo Please install Python and run this script again.
    pause
    exit /b 1
)

REM Check for Git
git --version >nul 2>&1
if errorlevel 1 (
    echo Git not found! Downloading ZIP instead...
    start https://github.com/khrehankashmiri/file_teleporter/archive/refs/heads/main.zip
    echo.
    echo Please extract the ZIP and run setup_windows.bat
    pause
    exit /b 1
)

REM Clone repository
echo Downloading File Teleporter...
git clone https://github.com/khrehankashmiri/file_teleporter.git
cd file_teleporter

REM Run setup
echo.
echo Running setup...
call setup_windows.bat

echo.
echo Installation complete!
echo Run: run_file_teleporter.bat
pause
