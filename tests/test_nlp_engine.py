"""Tests for NLP engine and similarity algorithms."""

import pytest
from src.nlp_engine import (
    tokenize,
    filter_stopwords,
    compute_tf_idf_similarity,
    extract_top_keywords,
    compute_vocabulary_overlap
)


def test_tokenize():
    text = "Building CI/CD pipelines with C++, Python, and scikit-learn."
    tokens = tokenize(text)
    assert "ci/cd" in tokens
    assert "c++" in tokens
    assert "python" in tokens
    assert "scikit-learn" in tokens


def test_filter_stopwords():
    tokens = ["the", "engineer", "was", "responsible", "for", "machine", "learning"]
    filtered = filter_stopwords(tokens)
    assert "the" not in filtered
    assert "was" not in filtered
    assert "responsible" not in filtered
    assert "engineer" in filtered
    assert "machine" in filtered
    assert "learning" in filtered


def test_tf_idf_identical_documents():
    text = "Senior Python developer experienced in Django, PostgreSQL, Docker, and AWS."
    score = compute_tf_idf_similarity(text, text)
    assert score >= 99.0


def test_tf_idf_disjoint_documents():
    doc1 = "Ancient history of Roman pottery and Latin poetry."
    doc2 = "Modern quantum computing algorithms in cryogenic semiconductor labs."
    score = compute_tf_idf_similarity(doc1, doc2)
    assert score < 15.0


def test_tf_idf_partial_match():
    resume = "Python software engineer building scalable web backends with PostgreSQL and Docker."
    jd = "Seeking a Senior Python Engineer with Docker, Kubernetes, and PostgreSQL experience."
    score = compute_tf_idf_similarity(resume, jd)
    assert 10.0 <= score <= 80.0


def test_extract_top_keywords():
    text = (
        "Machine learning models using PyTorch, natural language processing, "
        "and transformers for deep learning classification pipelines."
    )
    keywords = extract_top_keywords(text, top_n=5)
    assert len(keywords) > 0
    kw_terms = [kw[0] for kw in keywords]
    assert any("learning" in t or "machine" in t or "pytorch" in t for t in kw_terms)


def test_compute_vocabulary_overlap():
    res = "Python, SQL, AWS, Docker"
    jd = "Python, AWS, Kubernetes, Terraform"
    overlap = compute_vocabulary_overlap(res, jd)
    assert overlap["shared_tokens_count"] >= 2
    assert overlap["jaccard_similarity"] > 0
