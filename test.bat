@echo off
setlocal

echo ======================================================================
echo    Running Automated Test Suite - Resume-Job Match Analyzer
echo ======================================================================
echo.

if not exist .venv\Scripts\pytest.exe (
    echo [ERROR] Virtual environment or pytest not detected.
    echo Please execute setup.bat first.
    exit /b 1
)

set PYTHONPATH=%~dp0;%PYTHONPATH%

.\.venv\Scripts\pytest -v --durations=10

if %errorlevel% neq 0 (
    echo.
    echo [FAIL] One or more tests failed.
    exit /b %errorlevel%
) else (
    echo.
    echo [PASS] All test cases executed successfully!
)
