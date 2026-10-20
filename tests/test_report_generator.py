"""Tests for report generator (JSON and HTML)."""

import json
import pytest
from src.report_generator import ReportGenerator


def test_generate_json_report():
    match_result = {
        "overall_score": 85.5,
        "tier": "High Match (ATS Pass Tier)",
        "skill_coverage_score": 88.0,
        "tfidf_similarity": 65.0,
        "matched_skills_count": 10,
        "total_jd_skills_count": 12,
        "missing_skills_count": 2,
        "matched_skills": ["Python", "PyTorch", "Docker"],
        "missing_skills": ["Kubernetes", "AWS"],
        "additional_skills": ["Tableau"],
        "missing_skills_by_priority": {"high": ["Kubernetes"], "medium": ["AWS"], "low": []}
    }
    ats_health = {
        "verb_impact_score": 90.0,
        "section_score": 100.0,
        "word_count": 520,
        "length_status": "Optimal",
        "strong_verbs_count": 8,
        "strong_verbs_found": ["architected", "engineered"],
        "weak_phrases_found": [],
        "metric_count": 5,
        "metric_matches": ["35%", "$4,200"],
        "sections_present": ["Summary", "Experience", "Skills", "Education"],
        "missing_critical_sections": []
    }
    recs = [
        {"priority": "HIGH", "category": "Keyword Optimization", "title": "Add Kubernetes", "description": "Desc", "action": "Act"}
    ]

    json_str = ReportGenerator.generate_json_report(match_result, ats_health, recs)
    parsed = json.loads(json_str)
    assert parsed["scores"]["overall_ats_score"] == 85.5
    assert parsed["scores"]["tier"] == "High Match (ATS Pass Tier)"
    assert len(parsed["actionable_recommendations"]) == 1


def test_generate_html_report():
    match_result = {
        "overall_score": 78.0,
        "tier": "Good Match (Competitive Tier)",
        "tier_color": "#3b82f6",
        "skill_coverage_score": 80.0,
        "tfidf_similarity": 55.0,
        "matched_skills_count": 8,
        "total_jd_skills_count": 10,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Docker"],
        "additional_skills": ["Git"],
        "missing_skills_by_priority": {"high": ["Docker"], "medium": [], "low": []}
    }
    ats_health = {
        "verb_impact_score": 75.0,
        "section_score": 85.0,
        "word_count": 480,
        "length_status": "Optimal",
        "strong_verbs_count": 5,
        "metric_count": 3,
        "weak_phrases_found": []
    }
    recs = []

    html_out = ReportGenerator.generate_html_report(match_result, ats_health, recs, candidate_name="Test User")
    assert "<!DOCTYPE html>" in html_out
    assert "Test User" in html_out
    assert "78.0%" in html_out
    assert "Python" in html_out
