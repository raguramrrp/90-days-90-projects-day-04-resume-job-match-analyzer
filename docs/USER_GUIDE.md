# User Guide: AI-Powered Resume–Job Compatibility Analyzer

Welcome to the **AI-Powered Resume–Job Compatibility Analyzer**! This guide walks you through using the application to audit your resume, target specific roles, and maximize your ATS pass rate.

---

## 1. Quick Launch
To start the application on Windows:
```cmd
run.bat
```
The browser will automatically open to `http://localhost:8501`.

---

## 2. Document Input Methods

### A. Uploading Documents
1. **Resume Input**: Under **"1. Candidate Resume"**, click the file uploader to select a file (`.pdf`, `.docx`, `.txt`, or `.md`).
   - The parser will automatically extract, clean, and populate the text area.
2. **Job Description Input**: Under **"2. Job Description"**, either upload a JD document or paste the text directly into the text box.

### B. Benchmark Demo Presets
If you want to immediately see how the system handles different candidate profiles, use the **Benchmark Demo Presets** dropdown in the sidebar:
- **Preset 1 (Senior AI Engineer ~85–95%)**: Strong match with deep NLP, PyTorch, Scikit-Learn, and AWS skills.
- **Preset 2 (Full-Stack Engineer vs AI JD ~50–65%)**: Moderate match demonstrating cross-discipline transition gaps.
- **Preset 3 (Junior Dev vs DevOps JD <50%)**: Low match highlighting extensive missing prerequisites.

---

## 3. Customizing ATS Scoring Weights
In the sidebar, expand **"⚙️ ATS Scoring Weights"** to adjust the relative importance of:
- **Skill Keyword Overlap** (Default: 45%)
- **TF-IDF Semantic Match** (Default: 35%)
- **Action Verbs & Impact** (Default: 10%)
- **Section Completeness** (Default: 10%)

If the total does not equal 100%, the application automatically normalizes the weights proportionally.

---

## 4. Understanding Analysis Tabs

### Tab 1: Compatibility Overview
- **ATS Gauge**: Visual gauge indicating your overall compatibility score and assigned tier:
  - 🟢 **85–100%**: High Match (ATS Pass Tier)
  - 🔵 **70–84%**: Good Match (Competitive Tier)
  - 🟡 **50–69%**: Moderate Match (Needs Optimization)
  - 🔴 **< 50%**: Low Match (Significant Gaps)
- **KPI Metrics**: Individual scores for Skill Coverage, Semantic Overlap, Action & Impact, and Section Completeness.
- **Radar Chart**: Visual comparison of your skills vs target job requirements across 8 core domains.
- **Top Keywords**: Horizontal bar chart showing highest-weighted n-grams from the job posting.

### Tab 2: Skill Gap Matrix
- **Matched Skills (Green)**: Technologies and competencies verified in both documents.
- **Missing Skills (Red & Amber)**: Categorized into:
  - 🔥 **High Priority**: Core required skills mentioned multiple times.
  - ⚡ **Medium Priority**: Secondary tools, libraries, and frameworks.
  - 🌱 **Nice to Have**: General or single-mention terms.
- **Candidate Value-Adds (Indigo)**: Extra skills you possess that exceed the minimum job requirements.

### Tab 3: Actionable ATS Recommendations
- **Priority Action Cards**: Specific recommendations outlining exactly what keywords to add and where.
- **Action Verb Audit**: List of detected active power verbs vs passive phrases that should be eliminated.
- **Quantifiable Metrics Check**: Breakdown of numbers, percentages, and metrics detected in your bullet points.

### Tab 4: Export Report
- **Download HTML Scorecard**: Self-contained, responsive HTML report suitable for offline viewing, printing, or portfolio inclusion.
- **Download JSON Report**: Machine-readable payload for automated ATS integrations or data pipelines.

---

## 5. Headless Command-Line Interface (CLI)
You can also run analyses directly from PowerShell / Command Prompt without starting the web UI:

```cmd
.\.venv\Scripts\python scripts\run_cli_analysis.py --resume data/sample_resumes/alex_chen_data_scientist.pdf --jd data/sample_jds/ai_data_scientist_job_description.txt --export-html reports/ats_scorecard.html --export-json reports/ats_report.json
```
