"""Tests for ATS analyzer, metrics audit, and recommendation generation."""

import pytest
from src.ats_analyzer import ATSAnalyzer


@pytest.fixture
def analyzer():
    return ATSAnalyzer()


def test_action_verbs_and_metrics_detection(analyzer):
    text = (
        "Architected an enterprise RAG pipeline and spearheaded model fine-tuning. "
        "Optimized inference latency by 35% and saved $4,200 monthly across 45,000 queries."
    )
    sections = {"Summary": "Summary text", "Experience": text, "Skills": "Python", "Education": "BS CS"}
    contacts = {"email": "alex@example.com", "phone": "555-1234", "linkedin": "in/alex"}

    health = analyzer.analyze_resume(text, sections, contacts)
    assert health["strong_verbs_count"] >= 3
    assert "architected" in health["strong_verbs_found"]
    assert "spearheaded" in health["strong_verbs_found"]
    assert "optimized" in health["strong_verbs_found"]
    assert health["metric_count"] >= 3
    assert health["impact_score"] >= 80.0


def test_weak_phrases_word_boundaries(analyzer):
    # 'candidate' contains 'did' as substring, but shouldn't trigger weak phrase 'did'
    text = "Candidate provided candidates with clear documentation and handled tickets."
    sections = {"Experience": text}
    contacts = {}

    health = analyzer.analyze_resume(text, sections, contacts)
    assert "did" not in health["weak_phrases_found"]
    assert "handled" in health["weak_phrases_found"]


def test_recommendation_generation(analyzer):
    match_result = {
        "overall_score": 58.0,
        "tfidf_similarity": 32.0,
        "missing_skills_by_priority": {
            "high": ["Kubernetes", "PyTorch"],
            "medium": ["Redis"],
            "low": []
        }
    }
    ats_health = {
        "metric_count": 1,
        "weak_phrases_found": ["worked on"],
        "missing_critical_sections": ["Education"],
        "missing_recommended_sections": [],
        "missing_contacts": ["LinkedIn Profile"]
    }

    recs = analyzer.generate_recommendations(match_result, ats_health)
    categories = [r["category"] for r in recs]
    assert "Keyword Optimization" in categories
    assert "Quantifiable Impact" in categories
    assert "Structure & Formatting" in categories
    assert "Contact Verification" in categories
