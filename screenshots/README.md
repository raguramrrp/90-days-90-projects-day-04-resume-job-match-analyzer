# Project Screenshots & Visual Tour

This directory contains real visual demonstration captures of the **AI-Powered Resume–Job Description Compatibility Analyzer** running on Windows with the redesigned workspace-first architecture.

## Captured Views

### 1. Workspace-First Step-by-Step UI Overview
**File:** `01_streamlit_dashboard_overview.png`  
**Description:** The primary redesigned interface featuring a compact sidebar (project identity only), top toolbar actions (`⚡ Presets`, `⚙️ Settings`, `ℹ️ About`), the 4-stage workflow ribbon (`Step 1: Resume` &bull; `Step 2: Job Description` &bull; `Step 3: Review & Analyze` &bull; `Step 4: Results Dashboard`), and an intuitive empty state ready for input.

### 2. Standalone ATS Compatibility Scorecard Report
**File:** `02_ats_scorecard_report.png`  
**Description:** The complete, exportable HTML scorecard showing the composite ATS compatibility rating (Overall Score, Skill Coverage, Semantic TF-IDF Fit, Action & Impact Score, and Section Completeness), detailed matched and prioritized missing skills, quantifiable metrics audit, and prioritized actionable recommendations.

### 3. Active ATS Results Dashboard & Skill Gap Matrix
**File:** `03_results_dashboard_view.png`  
**Description:** The active results dashboard with Preset 1 (Senior AI Engineer) loaded and analyzed, displaying the interactive Plotly score radial gauge, 4 KPI cards, Domain Skill Radar Chart, Top Weighted JD Keywords bar chart, and the 4 interactive results tabs.

## How to Re-generate Screenshots
You can reproduce or refresh the screenshot assets at any time using the bundled capture utility:

```cmd
.\.venv\Scripts\python scripts\capture_screenshots.py
```
This utility uses Headless Google Chrome with the Chrome DevTools Protocol (CDP) to render and save genuine application screenshots.
