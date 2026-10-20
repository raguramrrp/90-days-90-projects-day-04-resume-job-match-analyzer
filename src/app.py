"""AI-Powered Resume-Job Description Compatibility Analyzer.

Main Streamlit Application Dashboard.
Day 4 — 90 Days 90 Projects Challenge.
"""

from __future__ import annotations

import os
import streamlit as st

from src.parser import (
    extract_text_from_file,
    extract_contact_info,
    extract_sections,
    DocumentParseError
)
from src.nlp_engine import compute_vocabulary_overlap
from src.skill_extractor import SkillExtractor
from src.matcher import CompatibilityMatcher
from src.ats_analyzer import ATSAnalyzer
from src.report_generator import ReportGenerator
from src.utils import (
    create_score_gauge,
    create_category_radar_chart,
    create_keyword_comparison_bar,
    load_sample_file
)

# Page configuration
st.set_page_config(
    page_title="AI Resume–Job Compatibility Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .kpi-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-metric {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }
    .skill-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 2px 4px 2px 0;
    }
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_services():
    """Initialize and cache core NLP services."""
    taxonomy_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills_taxonomy.json")
    skill_extractor = SkillExtractor(taxonomy_file_path=taxonomy_path)
    matcher = CompatibilityMatcher(skill_extractor=skill_extractor)
    ats_analyzer = ATSAnalyzer()
    return skill_extractor, matcher, ats_analyzer


skill_extractor, matcher, ats_analyzer = get_services()


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏆 90 Days 90 Projects")
    st.markdown("**Day 4:** Resume–Job Match Analyzer")
    st.caption("AI/NLP CareerTech Portfolio Project")
    st.markdown("---")

    st.markdown("### ⚡ Benchmark Demo Presets")
    st.caption("Click a preset below to instantly load candidate resumes and job descriptions:")
    
    preset = st.selectbox(
        "Choose a test profile:",
        [
            "Select custom or preset...",
            "Preset 1: Senior AI Engineer (High Match ~85-95%)",
            "Preset 2: Full-Stack Engineer vs AI JD (Moderate ~50-65%)",
            "Preset 3: Junior Dev vs Cloud DevOps JD (Gap Analysis <50%)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("### ⚙️ ATS Scoring Weights")
    with st.expander("Customize Algorithm Weights", expanded=False):
        w_skills = st.slider("Skill Keyword Overlap", 10, 70, 45, 5, help="Weight for exact and canonical skills coverage")
        w_tfidf = st.slider("TF-IDF Semantic Match", 10, 70, 35, 5, help="Weight for document-wide n-gram text similarity")
        w_impact = st.slider("Action Verbs & Impact", 0, 30, 10, 5, help="Weight for quantified metrics and power verbs")
        w_sections = st.slider("Section Completeness", 0, 30, 10, 5, help="Weight for standard ATS structural headings")
        
        total_w = w_skills + w_tfidf + w_impact + w_sections
        if total_w != 100:
            st.warning(f"Total weight is {total_w}%. Normalizing to 100%.")

    st.markdown("---")
    st.markdown("### 📖 About the Technology")
    st.caption(
        "Built using **scikit-learn** TF-IDF vectorization, cosine similarity, "
        "and a multi-word taxonomy matching engine. Parses PDF, DOCX, and TXT documents."
    )


# --- MAIN HEADER ---
st.markdown("<div class='main-title'>📄 AI-Powered Resume–Job Compatibility Analyzer</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Evaluate resume compatibility against any job description, uncover critical skill gaps, "
    "audit ATS compliance, and receive prioritized recommendations.</div>",
    unsafe_allow_html=True
)

# Preset data resolution
resume_default_text = ""
jd_default_text = ""

if preset == "Preset 1: Senior AI Engineer (High Match ~85-95%)":
    resume_default_text = load_sample_file("data/sample_resumes/alex_chen_data_scientist.txt")
    jd_default_text = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
elif preset == "Preset 2: Full-Stack Engineer vs AI JD (Moderate ~50-65%)":
    resume_default_text = load_sample_file("data/sample_resumes/priya_patel_fullstack_dev.txt")
    jd_default_text = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
elif preset == "Preset 3: Junior Dev vs Cloud DevOps JD (Gap Analysis <50%)":
    resume_default_text = load_sample_file("data/sample_resumes/marcus_vance_junior_developer.txt")
    jd_default_text = load_sample_file("data/sample_jds/devops_cloud_engineer_job_description.txt")


# --- INPUT INTERFACE ---
col_res, col_jd = st.columns(2)

with col_res:
    st.markdown("#### 1. Candidate Resume")
    resume_file = st.file_uploader(
        "Upload Resume (.pdf, .docx, .txt)",
        type=["pdf", "docx", "txt", "md"],
        help="Upload candidate resume in PDF, Word DOCX, or Plain Text format"
    )
    
    extracted_resume_text = ""
    if resume_file is not None:
        try:
            extracted_resume_text = extract_text_from_file(resume_file.read(), resume_file.name)
            st.success(f"Successfully extracted text from '{resume_file.name}' ({len(extracted_resume_text.split())} words)")
        except DocumentParseError as e:
            st.error(f"Error parsing resume: {e}")

    # Editable text area
    initial_resume_val = extracted_resume_text or resume_default_text
    resume_text = st.text_area(
        "Or edit / paste Resume content:",
        value=initial_resume_val,
        height=260,
        placeholder="Paste plain text resume here or use the file uploader above..."
    )

with col_jd:
    st.markdown("#### 2. Job Description")
    jd_file = st.file_uploader(
        "Upload Job Description (Optional)",
        type=["pdf", "docx", "txt", "md"],
        help="Upload JD file or paste text directly into the box below"
    )
    
    extracted_jd_text = ""
    if jd_file is not None:
        try:
            extracted_jd_text = extract_text_from_file(jd_file.read(), jd_file.name)
            st.success(f"Successfully extracted text from '{jd_file.name}' ({len(extracted_jd_text.split())} words)")
        except DocumentParseError as e:
            st.error(f"Error parsing job description: {e}")

    initial_jd_val = extracted_jd_text or jd_default_text
    jd_text = st.text_area(
        "Or edit / paste Job Description:",
        value=initial_jd_val,
        height=260,
        placeholder="Paste full job description, requirements, and responsibilities here..."
    )

# Action button
analyze_clicked = st.button("🚀 Run Compatibility Analysis", type="primary", use_container_width=True)

# Preserve state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if analyze_clicked:
    if not resume_text.strip():
        st.error("Please provide a resume by uploading a document or pasting text.")
    elif not jd_text.strip():
        st.error("Please provide a job description by uploading a document or pasting text.")
    else:
        st.session_state.analysis_done = True
        st.session_state.resume_text = resume_text
        st.session_state.jd_text = jd_text


# --- RESULTS DISPLAY ---
if st.session_state.analysis_done and "resume_text" in st.session_state:
    res_text = st.session_state.resume_text
    j_text = st.session_state.jd_text

    with st.spinner("Analyzing document compatibility, extracting skills, and auditing ATS metrics..."):
        # 1. Parsing & Section Extraction
        sections = extract_sections(res_text)
        contacts = extract_contact_info(res_text)

        # 2. ATS Health & Quality Audit
        ats_health = ats_analyzer.analyze_resume(res_text, sections, contacts)

        # 3. Matching & Similarity
        # Normalize custom weights
        total_weight = w_skills + w_tfidf + w_impact + w_sections
        norm_w_skills = w_skills / total_weight
        norm_w_tfidf = w_tfidf / total_weight
        norm_w_impact = w_impact / total_weight
        norm_w_sec = w_sections / total_weight

        match_result = matcher.match(
            res_text, 
            j_text, 
            section_score=ats_health["section_score"],
            verb_impact_score=ats_health["verb_impact_score"]
        )

        # Re-apply custom weights if customized
        custom_overall = (
            (match_result["skill_coverage_score"] * norm_w_skills) +
            (match_result["tfidf_similarity"] * norm_w_tfidf) +
            (ats_health["verb_impact_score"] * norm_w_impact) +
            (ats_health["section_score"] * norm_w_sec)
        )
        match_result["overall_score"] = round(max(0.0, min(100.0, custom_overall)), 1)
        
        # Update tier color and name based on custom score
        if match_result["overall_score"] >= 85:
            match_result["tier"] = "High Match (ATS Pass Tier)"
            match_result["tier_color"] = "#10b981"
        elif match_result["overall_score"] >= 70:
            match_result["tier"] = "Good Match (Competitive Tier)"
            match_result["tier_color"] = "#3b82f6"
        elif match_result["overall_score"] >= 50:
            match_result["tier"] = "Moderate Match (Needs Optimization)"
            match_result["tier_color"] = "#f59e0b"
        else:
            match_result["tier"] = "Low Match (Significant Gaps)"
            match_result["tier_color"] = "#ef4444"

        # 4. Generate Recommendations
        recommendations = ats_analyzer.generate_recommendations(match_result, ats_health)

        # Extract categorized skills for radar chart
        res_skills_data = skill_extractor.extract_skills(res_text)
        jd_skills_data = skill_extractor.extract_skills(j_text)

    st.markdown("---")

    # TABS FOR NAVIGATION
    tab_overview, tab_skills, tab_recs, tab_export = st.tabs([
        "📊 Compatibility Overview", 
        "🔍 Skill Gap Matrix", 
        "💡 Actionable ATS Recommendations", 
        "📥 Export Report"
    ])

    # === TAB 1: OVERVIEW ===
    with tab_overview:
        col_gauge, col_kpis = st.columns([1.1, 1.9])

        with col_gauge:
            gauge_fig = create_score_gauge(
                match_result["overall_score"], 
                match_result["tier"], 
                match_result["tier_color"]
            )
            st.plotly_chart(gauge_fig, use_container_width=True)

        with col_kpis:
            k1, k2 = st.columns(2)
            with k1:
                st.markdown(
                    f"""<div class='kpi-box' style='border-top:3px solid #3b82f6;'>
                        <div class='kpi-title'>Skill Keyword Coverage</div>
                        <div class='kpi-metric' style='color:#3b82f6;'>{match_result['skill_coverage_score']}%</div>
                        <span style='font-size:0.8rem; color:#64748b;'>{match_result['matched_skills_count']} of {match_result['total_jd_skills_count']} required skills matched</span>
                    </div>""", 
                    unsafe_allow_html=True
                )
            with k2:
                st.markdown(
                    f"""<div class='kpi-box' style='border-top:3px solid #8b5cf6;'>
                        <div class='kpi-title'>Semantic TF-IDF Match</div>
                        <div class='kpi-metric' style='color:#8b5cf6;'>{match_result['tfidf_similarity']}%</div>
                        <span style='font-size:0.8rem; color:#64748b;'>Document vocabulary & n-gram overlap</span>
                    </div>""", 
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            k3, k4 = st.columns(2)
            with k3:
                st.markdown(
                    f"""<div class='kpi-box' style='border-top:3px solid #10b981;'>
                        <div class='kpi-title'>Action Verbs & Impact</div>
                        <div class='kpi-metric' style='color:#10b981;'>{ats_health['verb_impact_score']}%</div>
                        <span style='font-size:0.8rem; color:#64748b;'>{ats_health['metric_count']} metrics, {ats_health['strong_verbs_count']} power verbs</span>
                    </div>""", 
                    unsafe_allow_html=True
                )
            with k4:
                st.markdown(
                    f"""<div class='kpi-box' style='border-top:3px solid #f59e0b;'>
                        <div class='kpi-title'>Section Completeness</div>
                        <div class='kpi-metric' style='color:#f59e0b;'>{ats_health['section_score']}%</div>
                        <span style='font-size:0.8rem; color:#64748b;'>{len(ats_health['sections_present'])} standard sections indexed</span>
                    </div>""", 
                    unsafe_allow_html=True
                )

        st.markdown("---")
        col_chart_left, col_chart_right = st.columns(2)

        with col_chart_left:
            st.markdown("#### 🎯 Domain Skill Competency Comparison")
            radar_fig = create_category_radar_chart(
                res_skills_data["by_category"], 
                jd_skills_data["by_category"]
            )
            st.plotly_chart(radar_fig, use_container_width=True)

        with col_chart_right:
            st.markdown("#### 🔑 Top Weighted Keywords in Job Description")
            bar_fig = create_keyword_comparison_bar(match_result["top_jd_keywords"])
            st.plotly_chart(bar_fig, use_container_width=True)

    # === TAB 2: SKILL GAP MATRIX ===
    with tab_skills:
        st.markdown("### Detailed Skill Alignment & Gap Analysis")
        st.caption("Detailed inventory of matched competencies, missing role prerequisites, and candidate value-add skills.")

        c_match, c_miss, c_extra = st.columns(3)

        with c_match:
            st.markdown(f"#### ✅ Matched Skills ({len(match_result['matched_skills'])})")
            if match_result["matched_skills"]:
                for s in match_result["matched_skills"]:
                    st.markdown(f"<span class='skill-pill' style='background:#d1fae5; color:#065f46;'>✓ {s}</span>", unsafe_allow_html=True)
            else:
                st.info("No matching skills detected from the predefined taxonomy.")

        with c_miss:
            st.markdown(f"#### ❌ Missing JD Skills ({len(match_result['missing_skills'])})")
            
            high = match_result["missing_skills_by_priority"]["high"]
            med = match_result["missing_skills_by_priority"]["medium"]
            low = match_result["missing_skills_by_priority"]["low"]

            if high:
                st.markdown("**🔥 High Priority (Core / Repeated):**")
                for s in high:
                    st.markdown(f"<span class='skill-pill' style='background:#fee2e2; color:#991b1b;'>⚠️ {s}</span>", unsafe_allow_html=True)

            if med:
                st.markdown("**⚡ Medium Priority (Frameworks & Tools):**")
                for s in med:
                    st.markdown(f"<span class='skill-pill' style='background:#fef3c7; color:#92400e;'>• {s}</span>", unsafe_allow_html=True)

            if low:
                st.markdown("**🌱 Nice to Have:**")
                for s in low:
                    st.markdown(f"<span class='skill-pill' style='background:#f1f5f9; color:#475569;'>• {s}</span>", unsafe_allow_html=True)

            if not match_result["missing_skills"]:
                st.success("Outstanding! All required skills from the job description are present.")

        with c_extra:
            st.markdown(f"#### ✨ Candidate Value-Adds ({len(match_result['additional_skills'])})")
            st.caption("Skills you have that exceed target requirements:")
            if match_result["additional_skills"]:
                for s in match_result["additional_skills"][:25]:
                    st.markdown(f"<span class='skill-pill' style='background:#e0e7ff; color:#3730a3;'>+ {s}</span>", unsafe_allow_html=True)
            else:
                st.info("No additional skills detected.")

    # === TAB 3: RECOMMENDATIONS & ATS HEALTH ===
    with tab_recs:
        st.markdown("### 💡 Prioritized ATS Optimization Roadmap")
        st.caption("Implement these targeted recommendations to maximize your resume's score across modern ATS parsers.")

        for rec in recommendations:
            badge_bg = "#ef4444" if rec["priority"] == "HIGH" else "#f59e0b"
            st.markdown(
                f"""<div class='rec-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h4 style='margin:0; color:#0f172a; font-size:1.05rem;'>{rec['title']}</h4>
                        <span class='badge' style='background:{badge_bg}; color:#ffffff;'>{rec['priority']} PRIORITY</span>
                    </div>
                    <p style='color:#475569; font-size:0.92rem; margin:8px 0 10px 0;'>{rec['description']}</p>
                    <div style='background:#f0fdfa; border-radius:6px; padding:8px 12px; font-size:0.85rem; color:#0f766e;'>
                        <b>Action Step:</b> {rec['action']}
                    </div>
                </div>""",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 📋 Resume Health & Structure Audit")

        r1, r2 = st.columns(2)
        with r1:
            st.markdown("#### Document Formatting & Length")
            st.write(f"- **Word Count:** {ats_health['word_count']} words")
            st.write(f"- **Length Assessment:** {ats_health['length_status']}")
            st.write(f"- **Sections Detected:** {', '.join(ats_health['sections_present'])}")
            if ats_health["missing_critical_sections"]:
                st.warning(f"Missing Critical Sections: {', '.join(ats_health['missing_critical_sections'])}")
            else:
                st.success("All critical sections (Experience, Skills, Education) are present.")

        with r2:
            st.markdown("#### Language & Quantifiable Impact")
            st.write(f"- **Power Action Verbs:** {ats_health['strong_verbs_count']} detected")
            if ats_health["strong_verbs_found"]:
                st.caption(f"Sample verbs: {', '.join(ats_health['strong_verbs_found'][:10])}")
            
            st.write(f"- **Measurable Metrics:** {ats_health['metric_count']} metrics identified")
            if ats_health["metric_matches"]:
                st.caption(f"Sample metrics: {', '.join(ats_health['metric_matches'][:6])}")

            if ats_health["weak_phrases_found"]:
                st.warning(f"Passive phrases to eliminate: {', '.join(ats_health['weak_phrases_found'])}")

    # === TAB 4: EXPORT REPORT ===
    with tab_export:
        st.markdown("### 📥 Download Analysis Reports")
        st.caption("Save your ATS compatibility audit for personal tracking, portfolio presentation, or sharing with a career mentor.")

        candidate_name = contacts.get("email") or "Candidate"
        if candidate_name and "@" in candidate_name:
            candidate_name = candidate_name.split("@")[0].replace(".", " ").title()

        html_report = ReportGenerator.generate_html_report(
            match_result, 
            ats_health, 
            recommendations,
            candidate_name=candidate_name,
            job_title="Target Role"
        )

        json_report = ReportGenerator.generate_json_report(
            match_result, 
            ats_health, 
            recommendations,
            candidate_name=candidate_name,
            job_title="Target Role"
        )

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                label="📄 Download Formatted HTML Scorecard",
                data=html_report,
                file_name="ats_compatibility_scorecard.html",
                mime="text/html",
                use_container_width=True
            )
            st.caption("A standalone, responsive HTML report suitable for browser viewing, printing, and sharing.")

        with d2:
            st.download_button(
                label="💾 Download Structured JSON Report",
                data=json_report,
                file_name="ats_compatibility_report.json",
                mime="application/json",
                use_container_width=True
            )
            st.caption("Clean machine-readable payload containing all scores, keyword metrics, and recommendations.")

        st.markdown("---")
        with st.expander("Inspect Raw JSON Payload"):
            st.json(json_report)
