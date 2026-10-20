@echo off
setlocal EnableDelayedExpansion

echo ======================================================================
echo    AI-Powered Resume-Job Match Analyzer - Environment Setup
echo ======================================================================
echo.

:: 1. Detect Python runtime (prefer 3.12 or py launcher)
echo [1/5] Checking for compatible Python installation...
set PYTHON_CMD=

py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.12
    goto PYTHON_FOUND
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto PYTHON_FOUND
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto PYTHON_FOUND
)

echo [ERROR] No compatible Python installation found on system PATH.
echo Please install Python 3.10, 3.11, or 3.12 from https://www.python.org/
exit /b 1

:PYTHON_FOUND
echo Found Python via: %PYTHON_CMD%
%PYTHON_CMD% --version

:: 2. Create virtual environment
echo.
echo [2/5] Configuring virtual environment (.venv)...
if not exist .venv (
    echo Creating virtual environment at .venv...
    %PYTHON_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Existing .venv directory detected.
)

:: 3. Install dependencies
echo.
echo [3/5] Installing dependencies from requirements.txt...
.\.venv\Scripts\python -m pip install --upgrade pip >nul 2>&1
.\.venv\Scripts\pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    exit /b 1
)
echo Dependencies installed successfully.

:: 4. Ensure directories exist
echo.
echo [4/5] Initializing local directories...
if not exist data\sample_resumes mkdir data\sample_resumes
if not exist data\sample_jds mkdir data\sample_jds
if not exist screenshots mkdir screenshots
if not exist reports mkdir reports

:: 5. Generate sample benchmark documents (PDF, DOCX)
echo.
echo [5/5] Generating benchmark sample resumes (PDF and DOCX)...
.\.venv\Scripts\python scripts\generate_sample_docs.py
if %errorlevel% neq 0 (
    echo [WARNING] Sample document generator completed with warnings.
)

echo.
echo ======================================================================
echo    SETUP COMPLETE! You are ready to run the project.
echo    To launch the interactive dashboard, run:  run.bat
echo    To execute the automated test suite, run: test.bat
echo ======================================================================
echo.
pause
