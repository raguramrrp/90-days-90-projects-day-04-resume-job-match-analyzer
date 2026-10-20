"""ATS Compatibility Report Generator.

Exports analysis results into structured JSON and self-contained, publication-ready
HTML scorecards suitable for PDF printing and portfolio presentation.
"""

from __future__ import annotations

import datetime
import html
import json
from typing import Any, Dict, List


class ReportGenerator:
    """Generates styled HTML scorecards and JSON export payloads."""

    @staticmethod
    def generate_json_report(
        match_result: Dict[str, Any],
        ats_health: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        candidate_name: str = "Candidate",
        job_title: str = "Target Position"
    ) -> str:
        """Export analysis as formatted JSON string."""
        payload = {
            "metadata": {
                "report_title": "AI-Powered Resume-Job Description Compatibility Report",
                "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "candidate_name": candidate_name,
                "job_title": job_title,
                "engine_version": "1.0.0"
            },
            "scores": {
                "overall_ats_score": match_result.get("overall_score", 0.0),
                "tier": match_result.get("tier", "Unknown"),
                "skill_coverage_score": match_result.get("skill_coverage_score", 0.0),
                "tfidf_similarity_score": match_result.get("tfidf_similarity", 0.0),
                "verb_impact_score": ats_health.get("verb_impact_score", 0.0),
                "section_completeness_score": ats_health.get("section_score", 0.0)
            },
            "skills_analysis": {
                "total_required_skills": match_result.get("total_jd_skills_count", 0),
                "matched_skills_count": match_result.get("matched_skills_count", 0),
                "missing_skills_count": match_result.get("missing_skills_count", 0),
                "matched_skills": match_result.get("matched_skills", []),
                "missing_skills": match_result.get("missing_skills", []),
                "additional_candidate_skills": match_result.get("additional_skills", []),
                "missing_skills_by_priority": match_result.get("missing_skills_by_priority", {})
            },
            "ats_health_metrics": {
                "word_count": ats_health.get("word_count", 0),
                "length_status": ats_health.get("length_status", ""),
                "strong_verbs_count": ats_health.get("strong_verbs_count", 0),
                "strong_verbs_sample": ats_health.get("strong_verbs_found", [])[:15],
                "weak_phrases_found": ats_health.get("weak_phrases_found", []),
                "quantifiable_metrics_count": ats_health.get("metric_count", 0),
                "quantifiable_metrics_sample": ats_health.get("metric_matches", []),
                "sections_present": ats_health.get("sections_present", []),
                "missing_critical_sections": ats_health.get("missing_critical_sections", [])
            },
            "actionable_recommendations": recommendations
        }
        return json.dumps(payload, indent=2)

    @staticmethod
    def generate_html_report(
        match_result: Dict[str, Any],
        ats_health: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        candidate_name: str = "Candidate",
        job_title: str = "Target Position"
    ) -> str:
        """Generate a complete, self-contained HTML report with CSS styling."""
        timestamp = datetime.datetime.now().strftime("%B %d, %Y - %H:%M")
        score = match_result.get("overall_score", 0.0)
        tier = match_result.get("tier", "Unknown")
        tier_color = match_result.get("tier_color", "#2563eb")

        matched = match_result.get("matched_skills", [])
        missing_high = match_result.get("missing_skills_by_priority", {}).get("high", [])
        missing_med = match_result.get("missing_skills_by_priority", {}).get("medium", [])
        missing_low = match_result.get("missing_skills_by_priority", {}).get("low", [])
        additional = match_result.get("additional_skills", [])

        # Build skill tags HTML
        def build_tags(skills: List[str], bg: str, text_c: str) -> str:
            if not skills:
                return "<span style='color:#94a3b8; font-style:italic;'>None detected</span>"
            return " ".join([
                f"<span style='display:inline-block; margin:2px 4px 2px 0; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; background:{bg}; color:{text_c};'>{html.escape(s)}</span>"
                for s in skills
            ])

        matched_html = build_tags(matched, "#d1fae5", "#065f46")
        missing_high_html = build_tags(missing_high, "#fee2e2", "#991b1b")
        missing_med_html = build_tags(missing_med, "#fef3c7", "#92400e")
        missing_low_html = build_tags(missing_low, "#f1f5f9", "#475569")
        additional_html = build_tags(additional[:20], "#e0e7ff", "#3730a3")

        # Build recommendations HTML
        recs_html = ""
        for rec in recommendations:
            badge_color = "#ef4444" if rec["priority"] == "HIGH" else "#f59e0b"
            recs_html += f"""
            <div style="background:#ffffff; border-left:4px solid {badge_color}; border-radius:8px; padding:16px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:14px; font-weight:700; color:#1e293b;">{html.escape(rec['title'])}</span>
                    <span style="background:{badge_color}; color:#ffffff; font-size:10px; font-weight:800; padding:2px 8px; border-radius:4px;">{rec['priority']} PRIORITY</span>
                </div>
                <p style="font-size:13px; color:#475569; margin:4px 0 8px 0; line-height:1.5;">{html.escape(rec['description'])}</p>
                <div style="font-size:12px; color:#0f766e; background:#f0fdfa; padding:6px 10px; border-radius:4px; font-weight:600;">
                    &#9989; <b>Recommended Action:</b> {html.escape(rec['action'])}
                </div>
            </div>
            """

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ATS Resume Compatibility Report - {html.escape(candidate_name)}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
        margin: 0;
        padding: 30px;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        overflow: hidden;
    }}
    .header {{
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: #ffffff;
        padding: 28px 36px;
    }}
    .header h1 {{
        margin: 0 0 6px 0;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}
    .header .meta {{
        font-size: 13px;
        color: #93c5fd;
    }}
    .content {{
        padding: 32px 36px;
    }}
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }}
    .kpi-card {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
    }}
    .kpi-label {{
        font-size: 12px;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 600;
        margin-top: 4px;
    }}
    .section-title {{
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
    }}
    .grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 24px;
    }}
    .card {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px;
    }}
    .footer {{
        background: #f1f5f9;
        padding: 16px 36px;
        font-size: 12px;
        color: #64748b;
        text-align: center;
        border-top: 1px solid #e2e8f0;
    }}
</style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>AI-Powered Resume–Job Compatibility Report</h1>
        <div class="meta">
            Target Role: <b>{html.escape(job_title)}</b> &nbsp;|&nbsp; Candidate: <b>{html.escape(candidate_name)}</b> &nbsp;|&nbsp; Generated: {timestamp}
        </div>
    </div>

    <div class="content">
        <!-- KPI Overview -->
        <div class="kpi-grid">
            <div class="kpi-card" style="border-top: 4px solid {tier_color};">
                <div class="kpi-value" style="color:{tier_color};">{score}%</div>
                <div class="kpi-label">Overall ATS Score</div>
                <div style="font-size:11px; font-weight:700; color:{tier_color}; margin-top:4px;">{tier}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{match_result.get('skill_coverage_score', 0)}%</div>
                <div class="kpi-label">Skill Keyword Match</div>
                <div style="font-size:11px; color:#64748b; margin-top:4px;">{match_result.get('matched_skills_count', 0)} of {match_result.get('total_jd_skills_count', 0)} required</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{match_result.get('tfidf_similarity', 0)}%</div>
                <div class="kpi-label">Semantic TF-IDF Fit</div>
                <div style="font-size:11px; color:#64748b; margin-top:4px;">Cosine N-Gram Overlap</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{ats_health.get('verb_impact_score', 0)}%</div>
                <div class="kpi-label">Action & Impact Metric</div>
                <div style="font-size:11px; color:#64748b; margin-top:4px;">{ats_health.get('metric_count', 0)} quantified results</div>
            </div>
        </div>

        <!-- Skills Breakdown -->
        <div class="section-title">&#128269; Skills Comparison Matrix</div>
        <div class="grid-2">
            <div class="card">
                <h4 style="margin:0 0 10px 0; color:#065f46; font-size:14px;">&#9989; Matched Skills ({len(matched)})</h4>
                {matched_html}
            </div>
            <div class="card">
                <h4 style="margin:0 0 10px 0; color:#991b1b; font-size:14px;">&#10060; Missing Skills (High Priority: {len(missing_high)})</h4>
                {missing_high_html}
                <div style="margin-top:12px;">
                    <span style="font-size:11px; font-weight:700; color:#64748b;">Medium Priority:</span>
                    <div style="margin-top:4px;">{missing_med_html}</div>
                </div>
            </div>
        </div>

        <div class="card" style="margin-bottom:24px;">
            <h4 style="margin:0 0 8px 0; color:#3730a3; font-size:14px;">&#10024; Additional Candidate Competencies ({len(additional)})</h4>
            <div style="font-size:12px; color:#64748b; margin-bottom:8px;">Skills present on resume that provide value beyond base JD criteria:</div>
            {additional_html}
        </div>

        <!-- ATS Structural Health -->
        <div class="section-title">&#128221; ATS Structural Health & Content Quality</div>
        <div class="grid-2">
            <div class="card">
                <h4 style="margin:0 0 8px 0; font-size:13px; color:#0f172a;">Formatting & Length Check</h4>
                <p style="font-size:12px; margin:4px 0;"><b>Word Count:</b> {ats_health.get('word_count', 0)} words</p>
                <p style="font-size:12px; margin:4px 0;"><b>Length Status:</b> {ats_health.get('length_status', '')}</p>
                <p style="font-size:12px; margin:4px 0;"><b>Section Completeness:</b> {ats_health.get('section_score', 0)}%</p>
            </div>
            <div class="card">
                <h4 style="margin:0 0 8px 0; font-size:13px; color:#0f172a;">Verbs & Quantifiable Results</h4>
                <p style="font-size:12px; margin:4px 0;"><b>Strong Action Verbs:</b> {ats_health.get('strong_verbs_count', 0)} distinct power verbs</p>
                <p style="font-size:12px; margin:4px 0;"><b>Quantified Metric Bullets:</b> {ats_health.get('metric_count', 0)} metrics detected</p>
                <p style="font-size:12px; margin:4px 0;"><b>Passive Phrases Flagged:</b> {len(ats_health.get('weak_phrases_found', []))}</p>
            </div>
        </div>

        <!-- Actionable Recommendations -->
        <div class="section-title">&#128161; Priority ATS Optimization Recommendations</div>
        {recs_html}

    </div>

    <div class="footer">
        Generated by <b>AI-Powered Resume–Job Compatibility Analyzer</b> &bull; Professional ATS Screening Report
    </div>
</div>

</body>
</html>
"""
        return html_template
