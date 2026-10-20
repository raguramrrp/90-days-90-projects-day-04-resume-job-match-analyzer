"""ATS Best-Practice Analyzer and Recommendations Generator.

Analyzes resume formatting, action verbs, measurable metrics, section completeness,
and generates prioritized, actionable recommendations.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Tuple


STRONG_ACTION_VERBS: Set[str] = {
    "accelerated", "accomplished", "achieved", "acquired", "adapted", "administered",
    "advanced", "advocated", "amplified", "analyzed", "architected", "assembled",
    "authored", "automated", "boosted", "built", "calculated", "championed",
    "collaborated", "composed", "conceived", "conducted", "configured", "constructed",
    "converted", "coordinated", "created", "customized", "debugged", "decreased",
    "delivered", "deployed", "designed", "developed", "devised", "diagnosed",
    "directed", "discovered", "documented", "doubled", "drafted", "drove",
    "eliminated", "enabled", "enforced", "engineered", "enhanced", "established",
    "evaluated", "executed", "expanded", "expedited", "fabricated", "facilitated",
    "finalized", "fine-tuned", "formulated", "founded", "generated", "guided",
    "halved", "headed", "identified", "implemented", "improved", "increased",
    "initiated", "innovated", "inspected", "installed", "instituted", "integrated",
    "interpreted", "introduced", "invented", "investigated", "launched", "lead",
    "led", "leveraged", "managed", "maximized", "mentored", "migrated",
    "minimized", "modernized", "monitored", "negotiated", "optimized", "orchestrated",
    "organized", "overhauled", "oversaw", "pioneered", "planned", "prepared",
    "produced", "programmed", "promoted", "published", "re-engineered", "realized",
    "rebuilt", "redesigned", "reduced", "refined", "refactored", "remodeled",
    "reorganized", "replaced", "resolved", "restructured", "revamped", "reviewed",
    "revitalized", "saved", "scaled", "scheduled", "secured", "simplified",
    "spearheaded", "standardized", "streamlined", "strengthened", "structured",
    "supervised", "surpassed", "trained", "transformed", "unified", "upgraded",
    "validated", "visualized", "won", "yielded"
}

WEAK_ACTION_PHRASES: List[str] = [
    "responsible for", "duties included", "worked on", "assisted with", "helped with",
    "participated in", "involved in", "familiar with", "tasked with", "handled",
    "did", "tried to", "attempted", "support of", "supported"
]


class ATSAnalyzer:
    """Evaluates resume quality, formatting, action verbs, and impact metrics."""

    def analyze_resume(
        self, 
        resume_text: str, 
        sections: Dict[str, str], 
        contacts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive ATS health check and recommendation synthesis."""
        lowered = resume_text.lower()
        words = re.findall(r"\b[a-zA-Z0-9_-]+\b", lowered)
        word_count = len(words)

        # 1. Action Verbs Audit
        strong_verbs_found = sorted(list({w for w in words if w in STRONG_ACTION_VERBS}))
        
        weak_phrases_found = []
        for phrase in WEAK_ACTION_PHRASES:
            if re.search(rf"\b{re.escape(phrase)}\b", lowered):
                weak_phrases_found.append(phrase)

        # Verb score (based on variety and presence of strong action verbs)
        verb_score = min(100.0, len(strong_verbs_found) * 10.0)

        # 2. Measurable Metrics & Quantifiable Impact Audit
        # Regex for percentages, dollar amounts, numbers + units, multipliers (35%, $4k, 2.5M, 10x)
        metric_matches = re.findall(
            r"(?:\b\d+(?:\.\d+)?%|\$\d+(?:,\d+)*(?:\.\d+)?[kKmMbB]?|\b\d+(?:\.\d+)?\s*(?:x|times|hours|users|clients|transactions|engineers|analysts|days|months|years|queries)\b|\b\d{1,3}(?:,\d{3})+\b)",
            resume_text,
            re.IGNORECASE
        )
        metric_count = len(metric_matches)
        
        # Impact score
        if metric_count >= 6:
            impact_score = 100.0
        elif metric_count >= 3:
            impact_score = 80.0
        elif metric_count >= 1:
            impact_score = 55.0
        else:
            impact_score = 25.0

        # 3. Section Completeness Audit
        critical_sections = ["Experience", "Skills", "Education"]
        recommended_sections = ["Summary", "Projects", "Certifications"]
        
        present_critical = [sec for sec in critical_sections if sec in sections]
        present_recommended = [sec for sec in recommended_sections if sec in sections]
        
        crit_score = (len(present_critical) / len(critical_sections)) * 70.0
        rec_score = (len(present_recommended) / len(recommended_sections)) * 30.0
        section_score = round(crit_score + rec_score, 1)

        # 4. Contact Information Health
        missing_contacts = []
        if not contacts.get("email"):
            missing_contacts.append("Email Address")
        if not contacts.get("phone"):
            missing_contacts.append("Phone Number")
        if not contacts.get("linkedin"):
            missing_contacts.append("LinkedIn Profile")
        if not contacts.get("github"):
            missing_contacts.append("GitHub / Portfolio")

        # 5. Length & Structure Health
        if word_count < 250:
            length_status = "Too Short (under 250 words; may lack sufficient technical detail)"
        elif word_count <= 900:
            length_status = "Optimal (ideal 1-2 page length for ATS readability)"
        elif word_count <= 1400:
            length_status = "Acceptable (2 pages, ensure high keyword density and no fluff)"
        else:
            length_status = "Too Long (exceeds 1,400 words; consider condensing to 1-2 pages)"

        # Combined Impact & Verb metric
        verb_impact_combined = round((verb_score * 0.5) + (impact_score * 0.5), 1)

        return {
            "word_count": word_count,
            "length_status": length_status,
            "strong_verbs_found": strong_verbs_found,
            "strong_verbs_count": len(strong_verbs_found),
            "weak_phrases_found": weak_phrases_found,
            "metric_matches": metric_matches[:10],
            "metric_count": metric_count,
            "impact_score": impact_score,
            "verb_score": verb_score,
            "verb_impact_score": verb_impact_combined,
            "section_score": section_score,
            "sections_present": list(sections.keys()),
            "missing_critical_sections": [s for s in critical_sections if s not in sections],
            "missing_recommended_sections": [s for s in recommended_sections if s not in sections],
            "contacts_found": contacts,
            "missing_contacts": missing_contacts
        }

    def generate_recommendations(
        self,
        match_result: Dict[str, Any],
        ats_health: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Synthesize prioritized, actionable ATS improvement recommendations."""
        recommendations: List[Dict[str, Any]] = []

        # Rec 1: High Priority Missing Skills
        high_missing = match_result.get("missing_skills_by_priority", {}).get("high", [])
        if high_missing:
            sample_skills = ", ".join(high_missing[:6])
            recommendations.append({
                "priority": "HIGH",
                "category": "Keyword Optimization",
                "title": f"Integrate {len(high_missing)} High-Priority Role Keywords",
                "description": (
                    f"The job description heavily stresses skills that are missing from your resume: {sample_skills}. "
                    "Incorporate these into your Technical Skills section and demonstrate their practical application "
                    "within your Professional Experience bullet points."
                ),
                "action": f"Add {sample_skills} to relevant project or experience descriptions."
            })

        # Rec 2: Medium Priority Missing Skills
        med_missing = match_result.get("missing_skills_by_priority", {}).get("medium", [])
        if med_missing:
            sample_skills = ", ".join(med_missing[:5])
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Competency Coverage",
                "title": f"Expand Tooling & Frameworks ({sample_skills})",
                "description": (
                    f"Consider adding secondary technical competencies: {sample_skills}. "
                    "ATS scanners filter for related tools, libraries, and frameworks during initial parsing."
                ),
                "action": f"List {sample_skills} in your skills matrix or tooling stack."
            })

        # Rec 3: Measurable Quantifiable Impact
        if ats_health.get("metric_count", 0) < 4:
            recommendations.append({
                "priority": "HIGH",
                "category": "Quantifiable Impact",
                "title": "Quantify Achievements with Tangible Metrics",
                "description": (
                    "Only a few bullet points contain measurable metrics (percentages, dollar amounts, performance gains). "
                    "Top-tier resumes use the XYZ formula: 'Accomplished [X] as measured by [Y] by doing [Z]'."
                ),
                "action": "Add specific metrics like '% latency reduction', 'X analyst hours saved', or 'Y daily requests handled'."
            })

        # Rec 4: Weak Action Verbs Replacement
        weak_phrases = ats_health.get("weak_phrases_found", [])
        if weak_phrases:
            phrases_str = ", ".join([f"'{p}'" for p in weak_phrases[:4]])
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Action Verb Strength",
                "title": "Replace Passive & Weak Phrasing with Power Action Verbs",
                "description": (
                    f"Detected passive phrases: {phrases_str}. Replace passive expressions with decisive action verbs "
                    "such as 'Architected', 'Spearheaded', 'Engineered', 'Optimized', or 'Automated'."
                ),
                "action": f"Swap phrases like '{weak_phrases[0]}' with verbs like 'Delivered', 'Engineered', or 'Led'."
            })

        # Rec 5: Missing Sections
        missing_crit = ats_health.get("missing_critical_sections", [])
        missing_rec = ats_health.get("missing_recommended_sections", [])
        if missing_crit or missing_rec:
            all_missing = missing_crit + missing_rec
            recommendations.append({
                "priority": "HIGH" if missing_crit else "LOW",
                "category": "Structure & Formatting",
                "title": f"Add Standard Section Headers ({', '.join(all_missing)})",
                "description": (
                    f"Your resume appears to lack clear headings for: {', '.join(all_missing)}. "
                    "ATS parsers rely on standard section headings to index candidate history accurately."
                ),
                "action": f"Include distinct markdown or bold headings for {', '.join(all_missing)}."
            })

        # Rec 6: Missing Contact Information
        missing_contacts = ats_health.get("missing_contacts", [])
        if missing_contacts:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Contact Verification",
                "title": f"Ensure Header Includes: {', '.join(missing_contacts)}",
                "description": (
                    f"Could not reliably detect: {', '.join(missing_contacts)}. "
                    "ATS platforms require clean, unformatted header text for recruiter outreach."
                ),
                "action": "Place email, phone number, and LinkedIn/GitHub links plainly in the top header."
            })

        # Rec 7: TF-IDF Textual Overlap
        tfidf_score = match_result.get("tfidf_similarity", 0.0)
        if tfidf_score < 40.0:
            recommendations.append({
                "priority": "HIGH",
                "category": "Vocabulary Alignment",
                "title": "Align Industry Terminology with Job Description",
                "description": (
                    f"Overall text similarity is currently {tfidf_score}%. "
                    "Review the job description's specific phrasing (e.g. 'cross-functional collaboration', "
                    "'production pipelines', 'high-throughput') and mirror their phrasing where truthful."
                ),
                "action": "Adopt the terminology used in the target job posting to pass ATS semantic screening."
            })

        return recommendations
