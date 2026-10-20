# Quickstart Guide

Get the **AI-Powered Resume–Job Compatibility Analyzer** running in under 2 minutes.

---

## ⚡ Method 1: Automated Windows One-Click (Recommended)

1. **Double-click `setup.bat`** (or run `.\setup.bat` in Command Prompt / PowerShell):
   - Automatically detects Python 3.10–3.12.
   - Creates a dedicated virtual environment at `.venv`.
   - Installs all dependencies (`streamlit`, `scikit-learn`, `pypdf`, `python-docx`, `plotly`, `pytest`).
   - Generates sample benchmark resumes and job postings.

2. **Double-click `run.bat`**:
   - Launches the Streamlit dashboard.
   - Automatically opens `http://localhost:8501` in your default browser.

3. **Double-click `test.bat`**:
   - Runs the complete automated test suite (26 unit tests).

---

## 🛠️ Method 2: Manual Terminal Setup

### 1. Clone or Navigate to Directory
```cmd
cd 90-days-90-projects-day-04-resume-job-match-analyzer
```

### 2. Create Virtual Environment
```cmd
py -3.12 -m venv .venv
```

### 3. Activate Environment
```cmd
.\.venv\Scripts\activate
```

### 4. Install Dependencies
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Generate Benchmark Sample Documents
```cmd
python scripts\generate_sample_docs.py
```

### 6. Run Automated Tests
```cmd
pytest -v
```

### 7. Launch Dashboard
```cmd
streamlit run src/app.py
```

---

## 💻 Method 3: Command-Line (Headless Analysis)
Analyze a resume without opening a browser:

```cmd
python scripts\run_cli_analysis.py --resume data\sample_resumes\alex_chen_data_scientist.pdf --jd data\sample_jds\ai_data_scientist_job_description.txt --export-html reports\scorecard.html
```
Open `reports\scorecard.html` in any browser to review the visual scorecard!
