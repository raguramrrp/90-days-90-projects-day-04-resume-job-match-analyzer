"""Tests for compatibility matcher and scoring."""

import pytest
from src.skill_extractor import SkillExtractor
from src.matcher import CompatibilityMatcher


@pytest.fixture
def matcher():
    extractor = SkillExtractor()
    return CompatibilityMatcher(skill_extractor=extractor)


def test_perfect_skill_match(matcher):
    resume = "Expert in Python, Machine Learning, PyTorch, Docker, and AWS."
    jd = "Seeking engineer proficient in Python, Machine Learning, PyTorch, Docker, and AWS."
    result = matcher.match(resume, jd, section_score=100.0, verb_impact_score=100.0)
    
    assert result["overall_score"] >= 80.0
    assert result["skill_coverage_score"] == 100.0
    assert len(result["missing_skills"]) == 0
    assert result["matched_skills_count"] == 5


def test_partial_match_and_missing_priorities(matcher):
    resume = "Experienced in Python, SQL, and Git."
    jd = (
        "Seeking Senior AI Specialist. Must have deep experience in Python, PyTorch, "
        "Kubernetes, and AWS. Knowledge of SQL and Git required."
    )
    result = matcher.match(resume, jd, section_score=80.0, verb_impact_score=70.0)

    assert result["overall_score"] < 80.0
    assert "Python" in result["matched_skills"]
    assert "PyTorch" in result["missing_skills"] or "Pytorch" in result["missing_skills"]
    assert len(result["missing_skills_by_priority"]["high"]) > 0


def test_empty_inputs(matcher):
    res = matcher.match("", "")
    assert res["overall_score"] == 0.0
    assert res["tier"] == "Insufficient Input"
