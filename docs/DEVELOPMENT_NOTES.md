# Development Notes & Design Decisions

**Day 4 — 90 Days 90 Projects Challenge**  
**Author:** Raguram R

---

## 1. Design Decisions & Trade-Offs

### A. scikit-learn TF-IDF vs Heavy Transformer Embeddings
- **Decision:** Used `TfidfVectorizer` (with unigram + bigram n-grams and sublinear term frequency scaling) paired with a curated multi-word skills taxonomy.
- **Rationale:** 
  - Pure Python + scikit-learn runs instantaneously (under 50ms per match) with zero GPU requirement and minimal memory overhead (~30MB RAM).
  - Heavy transformer models (e.g., Sentence-Transformers `all-MiniLM-L6-v2`) require downloading 100–400MB models, torch dependencies, and increase initial cold-start latency to 8–15 seconds, creating friction for recruiters and job seekers running locally.
  - TF-IDF with exact keyword and phrase taxonomy matching closely mirrors how legacy and contemporary ATS parsers (Workday, Taleo, Greenhouse) actually index candidates.

### B. Pure Python Document Parsers (`pypdf` + `python-docx`)
- **Decision:** Avoided external C-based PDF tools (like Poppler, pdf2image, or Tesseract OCR) in favor of pure-Python `pypdf` and `python-docx`.
- **Rationale:** 
  - Ensures seamless Windows installation without requiring users to install external binary executables or set Windows environment PATH variables.
  - Handles 95%+ of digitally created resumes exported from Word, Canva, Overleaf/LaTeX, or Google Docs.

### C. Multi-Word Taxonomy Matching with Boundary Safety
- **Decision:** Built a reverse-indexed taxonomy matcher that checks longest phrases first (e.g., `"natural language processing"` before `"language"`).
- **Special Cases Handled:**
  - Single-letter programming languages like `C` and `R`: Regex requires explicit contextual phrasing (e.g., `C programming`, `language R`) so common words like `"a"`, `"c"`, or `"r"` don't cause false positives.
  - Programming symbols like `C++`, `C#`, and `.NET`: Standard `\b` word boundaries fail on symbols because `+` and `#` are non-word characters. Designed custom lookahead and lookbehind expressions:
    `(?<![\w#+])c\+\+(?![\w#+])`

### D. Multi-Factor Composite Scoring
- **Decision:** Combined 4 orthogonal metrics:
  1. **Canonical Skill Coverage (45%)**: Direct matching against job prerequisites.
  2. **TF-IDF Semantic Cosine Similarity (35%)**: Contextual document-wide terminology overlap.
  3. **Action Verbs & Quantifiable Impact (10%)**: Quality of bullet points and evidence of achievement.
  4. **Section Completeness (10%)**: Presence of expected ATS resume sections.
- **Rationale:** Avoids the flaw where a resume with high vocabulary overlap but missing core programming languages receives an artificially inflated score.

---

## 2. Taxonomy Schema
The taxonomy is structured in `data/skills_taxonomy.json` across 8 primary domains:
1. `Programming Languages`: 24 languages including Python, TypeScript, Java, Go, Rust, C++, C#, SQL.
2. `AI, ML & Data Science`: 48 competencies including NLP, LLMs, PyTorch, Scikit-Learn, Transformers, LangChain, RAG, ChromaDB.
3. `Web & App Frameworks`: 29 frameworks including React, Next.js, Node.js, Express, Django, FastAPI, Flutter.
4. `Cloud & DevOps`: 22 technologies including AWS, GCP, Azure, Docker, Kubernetes, Terraform, CI/CD.
5. `Databases & Storage`: 18 database engines including PostgreSQL, MongoDB, Redis, Snowflake, BigQuery.
6. `Software Engineering & Tools`: 24 engineering practices including Git, TDD, Agile, Microservices, Pytest.
7. `Soft Skills & Leadership`: 14 interpersonal competencies including Problem Solving, Leadership, Mentorship.
8. `Certifications & Education`: Standard degree credentials and professional certifications.

---

## 3. Performance & Memory Profile
- **Document Parse Latency:** ~15–35 ms for 2-page PDF/DOCX.
- **Skill Extraction Latency:** ~8–15 ms for 1,200+ taxonomy terms.
- **TF-IDF Vectorization & Similarity:** ~10–20 ms.
- **Total Pipeline Execution:** < 80 ms end-to-end.
- **Test Suite Runtime:** 26 tests executed in 4.54 seconds.
