# Testing & Quality Assurance Report

**Day 4 — 90 Days 90 Projects Challenge**  
**Author:** Raguram R  
**Test Suite:** `pytest`  
**Total Tests:** 26  
**Status:** PASS (26/26 passed, 100% success rate)  
**Execution Time:** 4.54 seconds  

---

## 1. Test Architecture & Coverage

The test suite is partitioned into 6 specialized modules under `tests/`:

| Module | Focus Area | Test Count | Status |
| :--- | :--- | :---: | :---: |
| `test_parser.py` | Text cleaning, PDF, DOCX, TXT parsers, contact info, section segmentation | 7 | **PASS** |
| `test_nlp_engine.py` | Tokenization, stopword removal, TF-IDF cosine similarity, n-grams, vocabulary overlap | 7 | **PASS** |
| `test_skill_extractor.py` | Single & multi-word skills, alias resolution, symbols (`c++`, `c#`, `.net`), domain categorization | 4 | **PASS** |
| `test_matcher.py` | Perfect match, partial match, priority ranking of missing skills, edge cases (empty text) | 3 | **PASS** |
| `test_ats_analyzer.py` | Power action verbs, weak phrases with word boundaries, quantifiable metrics detection, recommendations | 3 | **PASS** |
| `test_report_generator.py` | JSON structure validation, HTML scorecard formatting, CSS & entity escaping | 2 | **PASS** |
| **Total** | | **26** | **PASS** |

---

## 2. Key Test Cases Verified

### A. Document Parsing & Security
- **Empty / Corrupt Files:** Handled via `DocumentParseError` rather than uncaught exceptions.
- **Unsupported Extensions:** Safely rejected with clear user error messaging.
- **Contact Extraction:** Verified detection of emails, phone numbers, LinkedIn URLs, GitHub URLs, and portfolio domains while preventing email domains from masquerading as portfolio links.
- **Section Segmentation:** Verified regex matching of multi-word headers (`Professional Summary`, `Technical Skills`, `Work Experience`, `Education`).

### B. NLP & Text Similarity
- **Identical Document Cosine Similarity:** Verified $\ge 99.0\%$.
- **Disjoint Document Cosine Similarity:** Verified $< 15.0\%$.
- **Partial Overlap:** Verified appropriate calibration between $10.0\%$ and $80.0\%$.
- **Tokenization:** Verified extraction of complex technical tokens (`ci/cd`, `c++`, `scikit-learn`).

### C. Skill & Entity Extraction
- **Alias Resolution:** Verified that aliases like `k8s` resolve to `kubernetes`, `sklearn` to `scikit-learn`, `react.js` to `react`.
- **Symbol Preservation:** Verified that `C++`, `C#`, and `.NET` match without false positive word boundaries.
- **Categorization:** Verified correct classification across all 8 technical domains.

### D. ATS Quality & Action Verbs
- **Action Verbs:** Verified detection of strong verbs (`architected`, `spearheaded`, `optimized`).
- **Word Boundary Weak Phrases:** Confirmed that words like `candidate` or `provided` do not falsely trigger the weak phrase `did`.
- **Quantifiable Metrics:** Verified detection of percentages (`35%`), currency (`$4,200`), scale (`45,000 queries`), and time metrics.

---

## 3. How to Run Tests

### Windows Batch Runner
```cmd
test.bat
```

### Manual Command
```cmd
.\.venv\Scripts\pytest -v --durations=10
```
