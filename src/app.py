"""Resume-Job Description Compatibility Analyzer.

Main Streamlit Application Dashboard.
Workspace-First Step-by-Step Architecture.
"""

from __future__ import annotations

import os
import sys

# Ensure project root directory is always on sys.path regardless of execution directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

try:
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
except ImportError:
    from parser import (
        extract_text_from_file,
        extract_contact_info,
        extract_sections,
        DocumentParseError
    )
    from nlp_engine import compute_vocabulary_overlap
    from skill_extractor import SkillExtractor
    from matcher import CompatibilityMatcher
    from ats_analyzer import ATSAnalyzer
    from report_generator import ReportGenerator
    from utils import (
        create_score_gauge,
        create_category_radar_chart,
        create_keyword_comparison_bar,
        load_sample_file
    )

# Page configuration
st.set_page_config(
    page_title="Resume–Job Match Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise SaaS Design System Styling
st.markdown("""
<style>
    /* Base typography and background */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Navigation Header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 1.5rem;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .header-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        margin-top: 0.2rem;
    }
    
    /* Workflow Stage Cards */
    .stage-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .stage-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.85rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #f1f5f9;
    }
    .stage-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .stage-badge {
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
        background: #f1f5f9;
        color: #475569;
    }
    .stage-badge-success {
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    
    /* Workflow Step Progression Ribbon */
    .step-ribbon {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .step-pill {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.6rem 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
    }
    .step-pill.active {
        border-color: #2563eb;
        background: #eff6ff;
        color: #1d4ed8;
    }
    .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: #e2e8f0;
        color: #475569;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .step-pill.active .step-num {
        background: #2563eb;
        color: #ffffff;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .kpi-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0.35rem 0 0.2rem 0;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #64748b;
    }
    
    /* Skill Pills */
    .skill-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 2px 4px 3px 0;
    }
    
    /* Recommendation Card */
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    /* Empty state card */
    .empty-card {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        color: #64748b;
        margin-top: 1rem;
    }
    .empty-icon {
        font-size: 2.8rem;
        margin-bottom: 0.8rem;
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


# --- SESSION STATE INITIALIZATION ---
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "ta_resume" not in st.session_state:
    st.session_state.ta_resume = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "ta_jd" not in st.session_state:
    st.session_state.ta_jd = ""
if "resume_filename" not in st.session_state:
    st.session_state.resume_filename = ""
if "jd_filename" not in st.session_state:
    st.session_state.jd_filename = ""
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "w_skills" not in st.session_state:
    st.session_state.w_skills = 45
if "w_tfidf" not in st.session_state:
    st.session_state.w_tfidf = 35
if "w_impact" not in st.session_state:
    st.session_state.w_impact = 10
if "w_sections" not in st.session_state:
    st.session_state.w_sections = 10
if "active_preset_name" not in st.session_state:
    st.session_state.active_preset_name = ""
if "_last_resume_file_id" not in st.session_state:
    st.session_state._last_resume_file_id = None
if "_last_jd_file_id" not in st.session_state:
    st.session_state._last_jd_file_id = None

# Support URL query parameter for automated demo/screenshot initialization (?preset=1/2/3)
query_preset = st.query_params.get("preset")
if query_preset and not st.session_state.resume_text:
    if query_preset == "1":
        loaded_res = load_sample_file("data/sample_resumes/alex_chen_data_scientist.txt")
        loaded_jd = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
        st.session_state.resume_text = loaded_res
        st.session_state.ta_resume = loaded_res
        st.session_state.jd_text = loaded_jd
        st.session_state.ta_jd = loaded_jd
        st.session_state.resume_filename = "alex_chen_data_scientist.txt (Preset 1)"
        st.session_state.jd_filename = "ai_data_scientist_job_description.txt"
        st.session_state.active_preset_name = "Senior AI Engineer (High Match)"
        st.session_state.analysis_done = True
    elif query_preset == "2":
        loaded_res = load_sample_file("data/sample_resumes/priya_patel_fullstack_dev.txt")
        loaded_jd = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
        st.session_state.resume_text = loaded_res
        st.session_state.ta_resume = loaded_res
        st.session_state.jd_text = loaded_jd
        st.session_state.ta_jd = loaded_jd
        st.session_state.resume_filename = "priya_patel_fullstack_dev.txt (Preset 2)"
        st.session_state.jd_filename = "ai_data_scientist_job_description.txt"
        st.session_state.active_preset_name = "Full-Stack Dev vs AI JD (Moderate)"
        st.session_state.analysis_done = True
    elif query_preset == "3":
        loaded_res = load_sample_file("data/sample_resumes/marcus_vance_junior_developer.txt")
        loaded_jd = load_sample_file("data/sample_jds/devops_cloud_engineer_job_description.txt")
        st.session_state.resume_text = loaded_res
        st.session_state.ta_resume = loaded_res
        st.session_state.jd_text = loaded_jd
        st.session_state.ta_jd = loaded_jd
        st.session_state.resume_filename = "marcus_vance_junior_developer.txt (Preset 3)"
        st.session_state.jd_filename = "devops_cloud_engineer_job_description.txt"
        st.session_state.active_preset_name = "Junior Dev vs DevOps JD (Low Match)"
        st.session_state.analysis_done = True


# --- DEDICATED DIALOGS (SECONDARY PANELS) ---

@st.dialog("⚡ Benchmark Demo Presets")
def open_presets_dialog():
    """Modal drawer for selecting and loading benchmark profiles."""
    st.markdown(
        "Select a pre-configured candidate resume and target job description to immediately test the "
        "matching engine across different career scenarios:"
    )
    st.markdown("---")

    # Preset 1
    p1_col1, p1_col2 = st.columns([3, 1])
    with p1_col1:
        st.markdown("**1. Senior AI & Machine Learning Engineer**")
        st.caption("Target: Apex Innovations AI Engineer JD &bull; Candidate: Alex Chen (~85–95% High Match)")
    with p1_col2:
        if st.button("Load Preset 1", key="btn_p1", use_container_width=True):
            p1_res = load_sample_file("data/sample_resumes/alex_chen_data_scientist.txt")
            p1_jd = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
            st.session_state.resume_text = p1_res
            st.session_state.ta_resume = p1_res
            st.session_state.jd_text = p1_jd
            st.session_state.ta_jd = p1_jd
            st.session_state.resume_filename = "alex_chen_data_scientist.txt (Preset 1)"
            st.session_state.jd_filename = "ai_data_scientist_job_description.txt"
            st.session_state.active_preset_name = "Senior AI Engineer (High Match)"
            st.session_state._last_resume_file_id = None
            st.session_state._last_jd_file_id = None
            st.session_state.analysis_done = False
            st.rerun()

    st.markdown("---")

    # Preset 2
    p2_col1, p2_col2 = st.columns([3, 1])
    with p2_col1:
        st.markdown("**2. Full-Stack Engineer vs AI JD (Role Switch)**")
        st.caption("Target: Apex Innovations AI Engineer JD &bull; Candidate: Priya Patel (~50–65% Moderate Match)")
    with p2_col2:
        if st.button("Load Preset 2", key="btn_p2", use_container_width=True):
            p2_res = load_sample_file("data/sample_resumes/priya_patel_fullstack_dev.txt")
            p2_jd = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
            st.session_state.resume_text = p2_res
            st.session_state.ta_resume = p2_res
            st.session_state.jd_text = p2_jd
            st.session_state.ta_jd = p2_jd
            st.session_state.resume_filename = "priya_patel_fullstack_dev.txt (Preset 2)"
            st.session_state.jd_filename = "ai_data_scientist_job_description.txt"
            st.session_state.active_preset_name = "Full-Stack Dev vs AI JD (Moderate)"
            st.session_state._last_resume_file_id = None
            st.session_state._last_jd_file_id = None
            st.session_state.analysis_done = False
            st.rerun()

    st.markdown("---")

    # Preset 3
    p3_col1, p3_col2 = st.columns([3, 1])
    with p3_col1:
        st.markdown("**3. Junior Developer vs Senior Cloud DevOps JD**")
        st.caption("Target: SkyPulse Systems DevOps JD &bull; Candidate: Marcus Vance (<50% Gap Analysis)")
    with p3_col2:
        if st.button("Load Preset 3", key="btn_p3", use_container_width=True):
            p3_res = load_sample_file("data/sample_resumes/marcus_vance_junior_developer.txt")
            p3_jd = load_sample_file("data/sample_jds/devops_cloud_engineer_job_description.txt")
            st.session_state.resume_text = p3_res
            st.session_state.ta_resume = p3_res
            st.session_state.jd_text = p3_jd
            st.session_state.ta_jd = p3_jd
            st.session_state.resume_filename = "marcus_vance_junior_developer.txt (Preset 3)"
            st.session_state.jd_filename = "devops_cloud_engineer_job_description.txt"
            st.session_state.active_preset_name = "Junior Dev vs DevOps JD (Low Match)"
            st.session_state._last_resume_file_id = None
            st.session_state._last_jd_file_id = None
            st.session_state.analysis_done = False
            st.rerun()

    st.markdown("---")
    c_close, c_clear = st.columns(2)
    with c_clear:
        if st.button("🔄 Clear Workspace", key="btn_clear_presets", use_container_width=True):
            st.session_state.resume_text = ""
            st.session_state.ta_resume = ""
            st.session_state.jd_text = ""
            st.session_state.ta_jd = ""
            st.session_state.resume_filename = ""
            st.session_state.jd_filename = ""
            st.session_state.active_preset_name = ""
            st.session_state._last_resume_file_id = None
            st.session_state._last_jd_file_id = None
            st.session_state.analysis_done = False
            st.rerun()


@st.dialog("⚙️ ATS Scoring Weights & Algorithm Settings")
def open_settings_dialog():
    """Modal drawer for tuning multi-factor ATS scoring algorithm weights."""
    st.markdown(
        "Customize the relative influence of each dimension in the composite ATS compatibility calculation. "
        "Weights are dynamically normalized to 100%:"
    )
    
    new_skills = st.slider(
        "Skill Keyword Overlap", 
        min_value=10, max_value=70, 
        value=st.session_state.w_skills, step=5,
        help="Weight assigned to exact and canonical skill matches from the 1,200+ skill taxonomy."
    )
    new_tfidf = st.slider(
        "TF-IDF Semantic Similarity", 
        min_value=10, max_value=70, 
        value=st.session_state.w_tfidf, step=5,
        help="Weight assigned to document-wide unigram/bigram cosine similarity."
    )
    new_impact = st.slider(
        "Action Verbs & Measurable Impact", 
        min_value=0, max_value=30, 
        value=st.session_state.w_impact, step=5,
        help="Weight assigned to strong power verbs and quantified metric bullets (%, $, scale)."
    )
    new_sections = st.slider(
        "Section Completeness", 
        min_value=0, max_value=30, 
        value=st.session_state.w_sections, step=5,
        help="Weight assigned to structural resume headings (Experience, Skills, Education, etc.)."
    )

    tot = new_skills + new_tfidf + new_impact + new_sections
    if tot != 100:
        st.info(f"Total weight sum: {tot}%. The algorithm will normalize these proportions to 100%.")
    else:
        st.success("Total weights perfectly equal 100%.")

    st.markdown("---")
    col_save, col_reset = st.columns(2)
    with col_save:
        if st.button("💾 Apply & Save Settings", key="btn_save_weights", type="primary", use_container_width=True):
            st.session_state.w_skills = new_skills
            st.session_state.w_tfidf = new_tfidf
            st.session_state.w_impact = new_impact
            st.session_state.w_sections = new_sections
            st.rerun()
    with col_reset:
        if st.button("↺ Reset to Defaults (45/35/10/10)", key="btn_reset_weights", use_container_width=True):
            st.session_state.w_skills = 45
            st.session_state.w_tfidf = 35
            st.session_state.w_impact = 10
            st.session_state.w_sections = 10
            st.rerun()


# Dynamic Word Counts
current_res_words = len(st.session_state.get("resume_text", "").split())
current_jd_words = len(st.session_state.get("jd_text", "").split())


# --- CLEAN MINIMAL SIDEBAR ---
with st.sidebar:
    st.markdown("### 📄 Resume Matcher")
    st.caption("ATS Compatibility & Keyword Optimizer")
    st.markdown("---")

    st.markdown("#### 📌 Workspace Status")
    if current_res_words > 0:
        st.markdown(f"**Resume:** <span style='color:#059669; font-weight:600;'>✓ Ready ({current_res_words} words)</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Resume:** <span style='color:#94a3b8;'>⚪ Awaiting input</span>", unsafe_allow_html=True)

    if current_jd_words > 0:
        st.markdown(f"**Job Description:** <span style='color:#059669; font-weight:600;'>✓ Ready ({current_jd_words} words)</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Job Description:** <span style='color:#94a3b8;'>⚪ Awaiting input</span>", unsafe_allow_html=True)

    if st.session_state.analysis_done:
        st.markdown("**ATS Status:** <span style='color:#2563eb; font-weight:600;'>🟢 Analysis Complete</span>", unsafe_allow_html=True)
    else:
        st.markdown("**ATS Status:** <span style='color:#94a3b8;'>⚪ Not Run</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚡ Quick Actions")
    if st.button("⚡ Demo Presets", key="sb_btn_presets", use_container_width=True):
        open_presets_dialog()
    if st.button("⚙️ ATS Weights", key="sb_btn_settings", use_container_width=True):
        open_settings_dialog()
    if st.button("🔄 Reset Workspace", key="sb_btn_reset", use_container_width=True):
        st.session_state.resume_text = ""
        st.session_state.ta_resume = ""
        st.session_state.jd_text = ""
        st.session_state.ta_jd = ""
        st.session_state.resume_filename = ""
        st.session_state.jd_filename = ""
        st.session_state.active_preset_name = ""
        st.session_state._last_resume_file_id = None
        st.session_state._last_jd_file_id = None
        st.session_state.analysis_done = False
        st.rerun()


# --- TOP MAIN WORKSPACE TOOLBAR ---
tb_col_info, tb_col_actions = st.columns([2.0, 1.0])

with tb_col_info:
    st.markdown(
        "<div class='header-title'>📄 Resume–Job Match Analyzer</div>"
        "<div class='header-subtitle'>Enterprise ATS Compatibility & Keyword Gap Optimization Engine</div>",
        unsafe_allow_html=True
    )

with tb_col_actions:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        if st.button("⚡ Presets", key="top_btn_presets", use_container_width=True, help="Load pre-configured benchmark profiles"):
            open_presets_dialog()
    with a2:
        if st.button("⚙️ Settings", key="top_btn_settings", use_container_width=True, help="Configure ATS scoring algorithm weights"):
            open_settings_dialog()

st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

# Step progression ribbon
step1_active = "active" if not st.session_state.analysis_done else ""
step2_active = "active" if not st.session_state.analysis_done else ""
step3_active = "active" if not st.session_state.analysis_done and (current_res_words > 0 and current_jd_words > 0) else ""
step4_active = "active" if st.session_state.analysis_done else ""

st.markdown(f"""
<div class='step-ribbon'>
    <div class='step-pill {step1_active}'>
        <span class='step-num'>1</span> Candidate Resume
    </div>
    <div class='step-pill {step2_active}'>
        <span class='step-num'>2</span> Job Description
    </div>
    <div class='step-pill {step3_active}'>
        <span class='step-num'>3</span> Review & Analyze
    </div>
    <div class='step-pill {step4_active}'>
        <span class='step-num'>4</span> Results Dashboard
    </div>
</div>
""", unsafe_allow_html=True)


# --- WORKSPACE STEP-BY-STEP WORKFLOW ---
col_step1, col_step2 = st.columns(2)

# === STEP 1: CANDIDATE RESUME ===
with col_step1:
    res_badge = (
        f"<span class='stage-badge stage-badge-success'>✓ {current_res_words} words</span>" 
        if current_res_words > 0 else "<span class='stage-badge'>Required</span>"
    )
    st.markdown(
        f"""<div class='stage-header'>
            <div class='stage-title'><span>📄</span> Step 1: Candidate Resume</div>
            {res_badge}
        </div>""",
        unsafe_allow_html=True
    )
    
    resume_file = st.file_uploader(
        "Upload Resume (.pdf, .docx, .txt, .md)",
        type=["pdf", "docx", "txt", "md"],
        key="uploader_resume",
        help="Upload candidate resume in PDF, Word DOCX, or Plain Text format"
    )
    
    if resume_file is not None:
        file_id = f"{resume_file.name}_{resume_file.size}"
        if st.session_state.get("_last_resume_file_id") != file_id:
            try:
                parsed_text = extract_text_from_file(resume_file.read(), resume_file.name)
                st.session_state._last_resume_file_id = file_id
                st.session_state.resume_text = parsed_text
                st.session_state.ta_resume = parsed_text
                st.session_state.resume_filename = resume_file.name
                st.session_state.analysis_done = False
                st.rerun()
            except DocumentParseError as e:
                st.error(f"Parse error: {e}")

    # Editable text area
    def on_resume_edited():
        st.session_state.resume_text = st.session_state.ta_resume

    st.text_area(
        "Resume Content (Editable):",
        height=240,
        key="ta_resume",
        on_change=on_resume_edited,
        placeholder="Upload a document above or paste plain text resume here...",
        help="Edit resume text directly. Changes are automatically preserved."
    )
    # Sync in case value was modified directly
    st.session_state.resume_text = st.session_state.get("ta_resume", "")


# === STEP 2: JOB DESCRIPTION ===
with col_step2:
    jd_badge = (
        f"<span class='stage-badge stage-badge-success'>✓ {current_jd_words} words</span>" 
        if current_jd_words > 0 else "<span class='stage-badge'>Required</span>"
    )
    st.markdown(
        f"""<div class='stage-header'>
            <div class='stage-title'><span>🎯</span> Step 2: Target Job Description</div>
            {jd_badge}
        </div>""",
        unsafe_allow_html=True
    )
    
    jd_file = st.file_uploader(
        "Upload Job Description Document (Optional)",
        type=["pdf", "docx", "txt", "md"],
        key="uploader_jd",
        help="Optional: Upload job description file or paste text directly below"
    )
    
    if jd_file is not None:
        file_id = f"{jd_file.name}_{jd_file.size}"
        if st.session_state.get("_last_jd_file_id") != file_id:
            try:
                parsed_jd = extract_text_from_file(jd_file.read(), jd_file.name)
                st.session_state._last_jd_file_id = file_id
                st.session_state.jd_text = parsed_jd
                st.session_state.ta_jd = parsed_jd
                st.session_state.jd_filename = jd_file.name
                st.session_state.analysis_done = False
                st.rerun()
            except DocumentParseError as e:
                st.error(f"Parse error: {e}")

    # Editable text area
    def on_jd_edited():
        st.session_state.jd_text = st.session_state.ta_jd

    st.text_area(
        "Job Description Content (Editable):",
        height=240,
        key="ta_jd",
        on_change=on_jd_edited,
        placeholder="Paste full job description requirements and responsibilities here...",
        help="Edit job description text directly. Changes are automatically preserved."
    )
    # Sync in case value was modified directly
    st.session_state.jd_text = st.session_state.get("ta_jd", "")


# Re-evaluate live word counts after text areas render
live_res_words = len(st.session_state.get("resume_text", "").split())
live_jd_words = len(st.session_state.get("jd_text", "").split())


# === STEP 3: REVIEW & ANALYZE ===
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """<div class='stage-header' style='margin-bottom:0.5rem;'>
            <div class='stage-title'><span>⚡</span> Step 3: Review Inputs & Run Compatibility Engine</div>
        </div>""",
        unsafe_allow_html=True
    )
    
    col_rev_stat, col_rev_btn = st.columns([2.2, 1.2])

    with col_rev_stat:
        res_ready = live_res_words > 0
        jd_ready = live_jd_words > 0
        
        stat_chips = []
        if res_ready:
            stat_chips.append(f"<span style='color:#059669; font-weight:600;'>✓ Resume Ready ({live_res_words} words)</span>")
        else:
            stat_chips.append("<span style='color:#dc2626; font-weight:600;'>⚠️ Missing Resume</span>")

        if jd_ready:
            stat_chips.append(f"<span style='color:#059669; font-weight:600;'>✓ Job Description Ready ({live_jd_words} words)</span>")
        else:
            stat_chips.append("<span style='color:#dc2626; font-weight:600;'>⚠️ Missing Job Description</span>")

        weights_summary = (
            f"Weights: Skills {st.session_state.w_skills}% &bull; TF-IDF {st.session_state.w_tfidf}% &bull; "
            f"Impact {st.session_state.w_impact}% &bull; Sections {st.session_state.w_sections}%"
        )
        
        st.markdown(f"Status: {' &nbsp;|&nbsp; '.join(stat_chips)}", unsafe_allow_html=True)
        st.caption(weights_summary)

    with col_rev_btn:
        run_analysis = st.button("🚀 Run Compatibility Analysis", type="primary", use_container_width=True)

    if run_analysis:
        if live_res_words == 0:
            st.error("Please provide a resume in Step 1 before analyzing.")
        elif live_jd_words == 0:
            st.error("Please provide a job description in Step 2 before analyzing.")
        else:
            st.session_state.analysis_done = True


# === STEP 4: RESULTS DASHBOARD ===
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

if not st.session_state.analysis_done or live_res_words == 0 or live_jd_words == 0:
    # High-quality Empty State
    st.markdown("""
    <div class='empty-card'>
        <div class='empty-icon'>🎯</div>
        <h3 style='color:#0f172a; margin-top:0;'>Ready to Analyze Resume Compatibility</h3>
        <p style='max-width:540px; margin:0.5rem auto 1.5rem auto; font-size:0.95rem; line-height:1.5;'>
            Complete Steps 1 and 2 above with your candidate resume and target job description, then click 
            <b>'Run Compatibility Analysis'</b> to generate your ATS scorecard, skill gap matrix, and optimization roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_empty_l, c_empty_mid, c_empty_r = st.columns([1, 1.2, 1])
    with c_empty_mid:
        if st.button("⚡ Load Senior AI Engineer Demo Preset", key="empty_load_preset", use_container_width=True):
            loaded_res = load_sample_file("data/sample_resumes/alex_chen_data_scientist.txt")
            loaded_jd = load_sample_file("data/sample_jds/ai_data_scientist_job_description.txt")
            st.session_state.resume_text = loaded_res
            st.session_state.ta_resume = loaded_res
            st.session_state.jd_text = loaded_jd
            st.session_state.ta_jd = loaded_jd
            st.session_state.resume_filename = "alex_chen_data_scientist.txt (Preset 1)"
            st.session_state.jd_filename = "ai_data_scientist_job_description.txt"
            st.session_state.active_preset_name = "Senior AI Engineer (High Match)"
            st.session_state._last_resume_file_id = None
            st.session_state._last_jd_file_id = None
            st.session_state.analysis_done = True
            st.rerun()

else:
    # RUN REAL COMPATIBILITY ENGINE
    res_text = st.session_state.resume_text
    j_text = st.session_state.jd_text

    with st.spinner("Analyzing document compatibility, extracting skills, and auditing ATS metrics..."):
        # 1. Parsing & Section Extraction
        sections = extract_sections(res_text)
        contacts = extract_contact_info(res_text)

        # 2. ATS Health & Quality Audit
        ats_health = ats_analyzer.analyze_resume(res_text, sections, contacts)

        # 3. Matching & Similarity
        total_weight = (
            st.session_state.w_skills + 
            st.session_state.w_tfidf + 
            st.session_state.w_impact + 
            st.session_state.w_sections
        )
        norm_w_skills = st.session_state.w_skills / total_weight
        norm_w_tfidf = st.session_state.w_tfidf / total_weight
        norm_w_impact = st.session_state.w_impact / total_weight
        norm_w_sec = st.session_state.w_sections / total_weight

        match_result = matcher.match(
            res_text, 
            j_text, 
            section_score=ats_health["section_score"],
            verb_impact_score=ats_health["verb_impact_score"]
        )

        # Re-apply normalized user weights
        custom_overall = (
            (match_result["skill_coverage_score"] * norm_w_skills) +
            (match_result["tfidf_similarity"] * norm_w_tfidf) +
            (ats_health["verb_impact_score"] * norm_w_impact) +
            (ats_health["section_score"] * norm_w_sec)
        )
        match_result["overall_score"] = round(max(0.0, min(100.0, custom_overall)), 1)
        
        # Update tier classification
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

        # 5. Extract categorized skills for radar chart
        res_skills_data = skill_extractor.extract_skills(res_text)
        jd_skills_data = skill_extractor.extract_skills(j_text)

    # RESULTS DASHBOARD CONTAINER
    st.markdown(
        """<div class='stage-header' style='margin-top:1rem; margin-bottom:0.8rem;'>
            <div class='stage-title'><span>📈</span> Step 4: ATS Compatibility Results Dashboard</div>
        </div>""",
        unsafe_allow_html=True
    )

    # ALL 4 RESULT TABS PRESERVED
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
                    f"""<div class='kpi-card' style='border-top:3px solid #3b82f6;'>
                        <div class='kpi-title'>Skill Keyword Coverage</div>
                        <div class='kpi-val' style='color:#3b82f6;'>{match_result['skill_coverage_score']}%</div>
                        <div class='kpi-sub'>{match_result['matched_skills_count']} of {match_result['total_jd_skills_count']} required skills matched</div>
                    </div>""", 
                    unsafe_allow_html=True
                )
            with k2:
                st.markdown(
                    f"""<div class='kpi-card' style='border-top:3px solid #8b5cf6;'>
                        <div class='kpi-title'>Semantic TF-IDF Match</div>
                        <div class='kpi-val' style='color:#8b5cf6;'>{match_result['tfidf_similarity']}%</div>
                        <div class='kpi-sub'>Document vocabulary & n-gram overlap</div>
                    </div>""", 
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            k3, k4 = st.columns(2)
            with k3:
                st.markdown(
                    f"""<div class='kpi-card' style='border-top:3px solid #10b981;'>
                        <div class='kpi-title'>Action Verbs & Impact</div>
                        <div class='kpi-val' style='color:#10b981;'>{ats_health['verb_impact_score']}%</div>
                        <div class='kpi-sub'>{ats_health['metric_count']} metrics, {ats_health['strong_verbs_count']} power verbs</div>
                    </div>""", 
                    unsafe_allow_html=True
                )
            with k4:
                st.markdown(
                    f"""<div class='kpi-card' style='border-top:3px solid #f59e0b;'>
                        <div class='kpi-title'>Section Completeness</div>
                        <div class='kpi-val' style='color:#f59e0b;'>{ats_health['section_score']}%</div>
                        <div class='kpi-sub'>{len(ats_health['sections_present'])} standard sections indexed</div>
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
                        <span style='background:{badge_bg}; color:#ffffff; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:4px;'>{rec['priority']} PRIORITY</span>
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
