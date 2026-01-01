@echo off
REM File Teleporter - Advanced Build Script
REM Creates a standalone .exe with optimized settings

echo ========================================
echo File Teleporter - Advanced Build
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

REM Install PyInstaller if needed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build...
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)
if exist "FileTeleporter.spec" (
    del FileTeleporter.spec
)

echo.
echo Building executable with advanced options...
echo This may take 5-10 minutes...
echo.

REM Build with advanced options
pyinstaller ^
    --name="FileTeleporter" ^
    --onefile ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --optimize=2 ^
    --add-data "config.json;." ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --collect-all=PySide6 ^
    --exclude-module=tkinter ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    file_teleporter.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    call .venv\Scripts\deactivate.bat
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
echo Executable location: dist\FileTeleporter.exe
echo.
echo File size:
dir dist\FileTeleporter.exe | find "FileTeleporter.exe"
echo.
pause
