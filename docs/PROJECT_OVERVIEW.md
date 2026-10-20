# Project Overview: AI-Powered Resume–Job Description Compatibility Analyzer

**Day 4 — 90 Days 90 Projects Challenge**  
**Author:** Raguram R (raguramrrp)  
**Domain:** Natural Language Processing (NLP) / CareerTech / HR Tech  
**Difficulty:** Beginner to Intermediate  

---

## 1. Problem Statement
Job seekers and engineering graduates struggle to determine whether their resumes will pass automated Applicant Tracking Systems (ATS) and semantic recruiter screenings. Modern ATS systems filter candidates based on keyword frequency, technical skills coverage, section formatting, and phrase relevance. Without objective feedback, applicants either submit generic resumes with low interview conversion or attempt manual keyword stuffing that hurts readability.

## 2. Solution
The **AI-Powered Resume–Job Description Compatibility Analyzer** provides transparent, multi-dimensional compatibility auditing. By parsing documents (PDF, DOCX, TXT), applying Natural Language Processing (TF-IDF vectorization, n-gram extraction, and taxonomy-based canonical skill matching), and evaluating structural ATS best practices, the tool delivers:
1. **Calibrated ATS Score (0–100%)**: Multi-factor weighted score combining semantic fit, skill keyword coverage, impact metrics, and structural integrity.
2. **Interactive Skill Gap Matrix**: Clear categorization of matched skills, missing skills (ranked by priority/urgency), and candidate bonus competencies.
3. **Actionable ATS Recommendations**: Specific guidance to replace passive phrasing, quantify bullet points, and integrate missing core keywords.
4. **Exportable Scorecards**: Publication-ready HTML scorecards and JSON reports.

## 3. Target Audience
- **Final-Year Students & Recent Graduates**: Preparing for placements, internships, and entry-level software engineering / data science roles.
- **Career Switchers**: Transitioning between domains (e.g. Full-Stack Web Development into Machine Learning/DevOps).
- **Recruiters & Mentors**: Quickly benchmarking candidate profiles against open requisitions.

## 4. MVP Boundaries & Scope
- **Included in Scope**:
  - Pure Python document parsing (PDF via `pypdf`, DOCX via `python-docx`, TXT with multiple encoding fallbacks).
  - TF-IDF document vectorization and cosine similarity calculation via `scikit-learn`.
  - Curated taxonomy of 1,200+ industry skills across 8 domains with alias resolution.
  - Action verb audit (strong vs weak phrasing) and quantifiable metrics detection.
  - Interactive Streamlit dashboard with Plotly radial gauges, radar charts, and horizontal bar charts.
  - Standalone HTML scorecard and JSON export generation.
  - Benchmark sample datasets (3 resumes, 3 job postings).
  - Windows one-click setup (`setup.bat`, `run.bat`, `test.bat`).
- **Deferred to Future Iterations**:
  - Dense semantic transformer embeddings (BERT / MiniLM) via Hugging Face.
  - Multi-language resume parsing.
  - Multi-candidate bulk screening dashboard for hiring teams.
