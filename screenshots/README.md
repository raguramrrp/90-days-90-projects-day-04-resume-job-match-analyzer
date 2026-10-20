# Project Screenshots & Visual Tour

This directory contains real visual demonstration captures of the **AI-Powered Resume–Job Description Compatibility Analyzer** running on Windows.

## Captured Views

### 1. Interactive Streamlit Dashboard Overview
**File:** `01_streamlit_dashboard_overview.png`  
**Description:** The primary interface featuring dual-pane document input (PDF/DOCX/TXT upload or text editing), pre-configured benchmark demo presets, and real-time ATS scoring weights customization in the sidebar.

### 2. Standalone ATS Compatibility Scorecard Report
**File:** `02_ats_scorecard_report.png`  
**Description:** The complete, exportable HTML scorecard showing the composite ATS compatibility rating (Overall Score, Skill Coverage, Semantic TF-IDF Fit, Action & Impact Score, and Section Completeness), detailed matched and prioritized missing skills, quantifiable metrics audit, and prioritized actionable recommendations.

## How to Re-generate Screenshots
You can reproduce or refresh the screenshot assets at any time using the bundled capture utility:

```cmd
.\.venv\Scripts\python scripts\capture_screenshots.py
```
This utility uses Headless Google Chrome with the Chrome DevTools Protocol (CDP) to render and save genuine application screenshots.
