@echo off
echo ========================================
echo iAmSmartGate - Reset Database
echo ========================================
echo.
echo WARNING: This will delete all existing data!
echo Press Ctrl+C to cancel, or
pause
echo.

echo Stopping any running servers...
taskkill /FI "WINDOWTITLE eq iAmSmartGate Backend*" /T /F 2>nul
taskkill /FI "WINDOWTITLE eq iAmSmartGate Admin Console*" /T /F 2>nul
timeout /t 2 /nobreak >nul
echo.

echo Deleting old database file...
cd backend
if exist instance\iamsmartgate.db (
    del /F /Q instance\iamsmartgate.db
    echo ✓ Database file deleted
) else (
    echo ℹ No existing database found
)

if exist instance (
    echo ✓ Instance folder exists
) else (
    mkdir instance
    echo ✓ Instance folder created
)
echo.

echo Database reset complete!
echo.
echo To start the system with fresh database, run: start.bat
echo.
pause
