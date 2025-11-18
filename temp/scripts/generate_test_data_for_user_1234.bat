@echo off
REM Generate synthetic test data for Organization 1234 and User user-d1850539

echo ========================================
echo Generating Synthetic Test Data
echo ========================================
echo.
echo Organization ID: 1234
echo User ID: user-d1850539
echo.

cd C:\Projects\MIRIX

python temp/scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-d1850539

echo.
echo ========================================
echo Data Generation Complete!
echo ========================================
echo.
echo Next: Run "streamlit run streamlit_app.py"
echo.
pause

