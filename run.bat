@echo off
setlocal

echo ======================================================================
echo    Starting AI-Powered Resume-Job Match Analyzer Dashboard
echo    Day 4 - 90 Days 90 Projects Challenge
echo ======================================================================

if not exist .venv\Scripts\streamlit.exe (
    echo [ERROR] Virtual environment or Streamlit not detected.
    echo Please execute setup.bat first to initialize dependencies.
    echo.
    pause
    exit /b 1
)

echo Activating environment and launching Streamlit web application...
echo Local URL: http://localhost:8501
echo Press Ctrl+C in this window to stop the server.
echo.

set PYTHONPATH=%~dp0;%PYTHONPATH%

.\.venv\Scripts\streamlit run src/app.py --server.port=8501 --server.headless=false

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Streamlit exited unexpectedly with code %errorlevel%.
    pause
)
