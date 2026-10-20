"""Tests for skill extractor and taxonomy matching."""

import pytest
from src.skill_extractor import SkillExtractor


@pytest.fixture
def extractor():
    return SkillExtractor()


def test_single_and_multiword_skills(extractor):
    text = (
        "Proficient in Python, machine learning, natural language processing, "
        "Docker, and scikit-learn."
    )
    res = extractor.extract_skills(text)
    skills = res["skills"]
    assert "python" in skills
    assert "machine learning" in skills
    assert "nlp" in skills or "natural language processing" in skills
    assert "docker" in skills
    assert "scikit-learn" in skills


def test_alias_normalization(extractor):
    text = "Experience with k8s, sklearn, tf, react.js, and nodejs."
    res = extractor.extract_skills(text)
    skills = res["skills"]
    assert "kubernetes" in skills
    assert "scikit-learn" in skills
    assert "tensorflow" in skills
    assert "react" in skills
    assert "node.js" in skills


def test_special_symbols_cpp_csharp_net(extractor):
    text = "Developed low-latency trading microservices in C++ and C# with .NET Core."
    res = extractor.extract_skills(text)
    skills = res["skills"]
    assert "c++" in skills
    assert "c#" in skills
    assert ".net" in skills


def test_categorization(extractor):
    text = "Python, PyTorch, AWS, PostgreSQL, Git, and Agile."
    res = extractor.extract_skills(text)
    by_cat = res["by_category"]
    assert "Programming Languages" in by_cat
    assert "AI, ML & Data Science" in by_cat
    assert "Cloud & DevOps" in by_cat
    assert "Databases & Storage" in by_cat
    assert "Software Engineering & Tools" in by_cat
