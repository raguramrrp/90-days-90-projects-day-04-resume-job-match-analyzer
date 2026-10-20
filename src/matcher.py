"""Compatibility Matcher and ATS Scoring Engine.

Combines TF-IDF textual similarity, canonical skill coverage, section completeness,
and keyword importance weighting into a calibrated ATS match report.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

try:
    from src.nlp_engine import compute_tf_idf_similarity, extract_top_keywords
    from src.skill_extractor import SkillExtractor
except ImportError:
    from nlp_engine import compute_tf_idf_similarity, extract_top_keywords
    from skill_extractor import SkillExtractor


class CompatibilityMatcher:
    """Evaluates compatibility between a candidate resume and a job description."""

    def __init__(self, skill_extractor: SkillExtractor):
        self.skill_extractor = skill_extractor

    def match(
        self, 
        resume_text: str, 
        jd_text: str,
        section_score: float = 100.0,
        verb_impact_score: float = 100.0
    ) -> Dict[str, Any]:
        """Perform comprehensive match analysis between resume and job description."""
        if not resume_text.strip() or not jd_text.strip():
            return {
                "overall_score": 0.0,
                "tier": "Insufficient Input",
                "tier_color": "#94a3b8",
                "tfidf_similarity": 0.0,
                "skill_coverage_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "additional_skills": [],
                "missing_skills_by_priority": {"high": [], "medium": [], "low": []},
                "total_jd_skills_count": 0,
                "matched_skills_count": 0,
                "missing_skills_count": 0,
                "top_jd_keywords": []
            }

        # 1. TF-IDF Cosine Similarity
        tfidf_sim = compute_tf_idf_similarity(resume_text, jd_text)

        # 2. Extract Skills from Resume and Job Description
        resume_skills_data = self.skill_extractor.extract_skills(resume_text)
        jd_skills_data = self.skill_extractor.extract_skills(jd_text)

        resume_skills_set = set(resume_skills_data["skills"])
        jd_skills_set = set(jd_skills_data["skills"])

        matched_skills_set = resume_skills_set.intersection(jd_skills_set)
        missing_skills_set = jd_skills_set.difference(resume_skills_set)
        additional_skills_set = resume_skills_set.difference(jd_skills_set)

        # 3. Skill Coverage Calculation
        total_jd_skills = len(jd_skills_set)
        if total_jd_skills > 0:
            skill_coverage = (len(matched_skills_set) / total_jd_skills) * 100.0
        else:
            skill_coverage = tfidf_sim  # Fallback if JD contains unusual or zero standard taxonomy keywords

        # 4. Priority Weighting for Missing Skills
        # High impact: Mentioned >= 2 times in JD or among top TF-IDF keywords
        jd_counts = jd_skills_data["skill_counts"]
        top_jd_kw_dict = dict(extract_top_keywords(jd_text, top_n=30))
        
        high_priority = []
        med_priority = []
        low_priority = []

        for skill in missing_skills_set:
            count = jd_counts.get(skill, 1)
            is_top_kw = skill in top_jd_kw_dict or any(skill in kw for kw in top_jd_kw_dict)
            category = self.skill_extractor.skill_to_category.get(skill, "")

            formatted_skill = skill.title() if len(skill) > 4 else skill.upper()

            if count >= 3 or (count >= 2 and is_top_kw) or category in {"Programming Languages", "AI, ML & Data Science"}:
                high_priority.append(formatted_skill)
            elif count >= 2 or is_top_kw or category in {"Cloud & DevOps", "Web & App Frameworks", "Databases & Storage"}:
                med_priority.append(formatted_skill)
            else:
                low_priority.append(formatted_skill)

        # 5. Composite Weighted ATS Score Calculation
        # Weights: 45% Skill Coverage, 35% TF-IDF Semantic Overlap, 10% Verb/Impact, 10% Section Completeness
        overall_score = (
            (skill_coverage * 0.45) +
            (tfidf_sim * 0.35) +
            (verb_impact_score * 0.10) +
            (section_score * 0.10)
        )
        overall_score = round(max(0.0, min(100.0, overall_score)), 1)

        # 6. ATS Match Tier
        if overall_score >= 85:
            tier = "High Match (ATS Pass Tier)"
            tier_color = "#10b981"  # Emerald green
        elif overall_score >= 70:
            tier = "Good Match (Competitive Tier)"
            tier_color = "#3b82f6"  # Blue
        elif overall_score >= 50:
            tier = "Moderate Match (Needs Optimization)"
            tier_color = "#f59e0b"  # Amber
        else:
            tier = "Low Match (Significant Gaps)"
            tier_color = "#ef4444"  # Red

        # Format skill lists for display
        def format_skill_list(skills: Set[str]) -> List[str]:
            return sorted([s.title() if len(s) > 4 else s.upper() for s in skills])

        return {
            "overall_score": overall_score,
            "tier": tier,
            "tier_color": tier_color,
            "tfidf_similarity": round(tfidf_sim, 1),
            "skill_coverage_score": round(skill_coverage, 1),
            "matched_skills": format_skill_list(matched_skills_set),
            "missing_skills": format_skill_list(missing_skills_set),
            "additional_skills": format_skill_list(additional_skills_set),
            "missing_skills_by_priority": {
                "high": sorted(high_priority),
                "medium": sorted(med_priority),
                "low": sorted(low_priority)
            },
            "total_jd_skills_count": total_jd_skills,
            "matched_skills_count": len(matched_skills_set),
            "missing_skills_count": len(missing_skills_set),
            "top_jd_keywords": extract_top_keywords(jd_text, top_n=15)
        }
