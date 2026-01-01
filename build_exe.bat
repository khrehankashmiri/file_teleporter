@echo off
REM File Teleporter - Build Executable Script
REM This script creates a standalone .exe file using PyInstaller

echo ========================================
echo File Teleporter - Build Executable
echo ========================================
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_windows.bat first.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller!
        echo.
        pause
        exit /b 1
    )
    echo.
)

echo Building executable...
echo This may take several minutes...
echo.

REM Build the executable
pyinstaller --name="FileTeleporter" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "config.json;." ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    file_teleporter.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo.
    pause
    exit /b 1
)

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The executable is located at:
echo   dist\FileTeleporter.exe
echo.
echo You can now:
echo   1. Run dist\FileTeleporter.exe directly
echo   2. Create a desktop shortcut to it
echo   3. Move it to any location on your computer
echo.
echo Note: The first run may take longer as it extracts files.
echo.
pause
