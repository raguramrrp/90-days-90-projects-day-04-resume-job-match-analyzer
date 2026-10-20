"""NLP Engine for Resume & Job Description Processing.

Provides TF-IDF vectorization, cosine similarity computation, n-gram extraction,
vocabulary overlap analysis, and keyword relevance scoring.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Comprehensive standard English stopwords list (plus common resume filler terms)
STANDARD_STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
    "yours", "yourself", "yourselves",
    # Common resume boilerplate tokens
    "responsible", "duties", "etc", "e.g.", "including", "per", "via", "well", "also"
}


def tokenize(text: str) -> List[str]:
    """Tokenize text into lower-cased alphanumeric words and tech terms (e.g. c++, c#, ci/cd, .net)."""
    if not text:
        return []
    # Match c++, c#, .net, or standard hyphenated/slashed tech tokens
    raw_tokens = re.findall(
        r"(?:\.net|[a-zA-Z0-9]+(?:\+\+|#)|[a-zA-Z0-9]+(?:[-_/][a-zA-Z0-9]+)*)", 
        text.lower()
    )
    return [t for t in raw_tokens if len(t) >= 2 or t in {"c", "r"}]


def filter_stopwords(tokens: List[str]) -> List[str]:
    """Remove standard stopwords from token sequence."""
    return [t for t in tokens if t not in STANDARD_STOPWORDS]


def compute_tf_idf_similarity(resume_text: str, jd_text: str) -> float:
    """Compute cosine similarity score (0.0 to 100.0) between resume and JD using TF-IDF."""
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,
        max_features=5000
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        raw_score = float(sim_matrix[0][0])
        # Return as percentage rounded to 1 decimal place
        return round(max(0.0, min(1.0, raw_score)) * 100, 1)
    except ValueError:
        return 0.0


def extract_top_keywords(text: str, top_n: int = 25) -> List[Tuple[str, float]]:
    """Extract top TF-IDF keywords and key phrases with their relative weights."""
    if not text.strip():
        return []
        
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=1000,
        sublinear_tf=True
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Sort terms by score descending
        term_scores = list(zip(feature_names, scores))
        term_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Filter purely numerical terms
        filtered = [
            (term, round(score, 4)) 
            for term, score in term_scores 
            if not term.replace(" ", "").isdigit() and len(term) > 2
        ]
        return filtered[:top_n]
    except ValueError:
        return []


def compute_vocabulary_overlap(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """Calculate token-level Jaccard similarity and vocabulary overlap."""
    resume_tokens = set(filter_stopwords(tokenize(resume_text)))
    jd_tokens = set(filter_stopwords(tokenize(jd_text)))
    
    if not jd_tokens:
        return {
            "jaccard_similarity": 0.0,
            "shared_tokens_count": 0,
            "jd_unique_tokens_count": 0,
            "resume_unique_tokens_count": len(resume_tokens)
        }
        
    shared = resume_tokens.intersection(jd_tokens)
    union = resume_tokens.union(jd_tokens)
    jaccard = (len(shared) / len(union)) * 100 if union else 0.0
    
    return {
        "jaccard_similarity": round(jaccard, 1),
        "shared_tokens_count": len(shared),
        "jd_unique_tokens_count": len(jd_tokens),
        "resume_unique_tokens_count": len(resume_tokens),
        "sample_shared_tokens": sorted(list(shared))[:20]
    }
