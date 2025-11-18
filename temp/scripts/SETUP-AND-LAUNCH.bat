@echo off
REM All-in-One Setup and Launch Script for MIRIX Temporal Memory Testing
REM Organization: 1234
REM User: user-d1850539

echo ========================================================================
echo MIRIX Temporal Memory System - Test Setup and Launch
echo ========================================================================
echo.
echo This script will:
echo   1. Generate 110 synthetic test memories
echo   2. Launch the Streamlit dashboard
echo.
echo Organization ID: 1234
echo User ID: user-d1850539
echo.
echo ========================================================================
pause

cd C:\Projects\MIRIX

echo.
echo Step 1: Generating synthetic test data...
echo ========================================================================
python temp/scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-d1850539

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Data generation failed!
    echo Check the error message above.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo Data generation complete!
echo ========================================================================
echo.
echo Step 2: Launching Streamlit dashboard...
echo ========================================================================
echo.
echo The dashboard will open in your browser automatically.
echo.
echo IMPORTANT: In the dashboard sidebar, enter:
echo   - Organization ID: 1234
echo   - User ID: user-d1850539
echo.
echo Press Ctrl+C in this window to stop the server when done.
echo ========================================================================
echo.
timeout /t 3

streamlit run streamlit_app.py

