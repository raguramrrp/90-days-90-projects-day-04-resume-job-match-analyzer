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

## 2. Navigation & Secondary Tool Panels

In the redesigned workspace-first layout, secondary tools are accessible via the top action toolbar:

- **⚡ Presets**: Opens the benchmark modal drawer to quickly load one of 3 realistic candidate-job pairings.
- **⚙️ Settings**: Opens the ATS algorithm scoring settings to customize weights for Skill Overlap, TF-IDF Similarity, Action Verbs, and Sections.
- **ℹ️ About**: Displays technology architecture, NLP algorithms, document parsing, and security/privacy principles.

The left sidebar is kept compact and clean, displaying only challenge identity, real-time input status, and quick shortcuts.

---

## 3. Step-by-Step Analysis Workflow

### Step 1: Candidate Resume
1. Drag and drop your resume file (`.pdf`, `.docx`, `.txt`, `.md`) or paste plain text into the editor.
2. The parser automatically extracts text, validates file contents, and displays word count metrics.
3. Edit the extracted text directly in the text area if you want to test adjustments in real-time.

### Step 2: Target Job Description
1. Paste the target job posting into the text area, or optionally upload a job description file (`.pdf`, `.docx`, `.txt`, `.md`).
2. The character and word counters will update immediately.

### Step 3: Review & Analyze
1. Review the input readiness indicators (e.g., `✓ Resume Ready (480 words)` &bull; `✓ Job Description Ready (310 words)`).
2. Click **🚀 Run Compatibility Analysis**.

### Step 4: Results Dashboard
Once executed, the results dashboard mounts smoothly below, featuring 4 comprehensive analysis tabs.

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
