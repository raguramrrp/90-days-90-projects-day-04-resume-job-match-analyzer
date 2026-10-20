"""Skill Extraction and Taxonomy Matching Engine.

Detects single-word and multi-word technical skills, libraries, frameworks,
databases, cloud platforms, and soft skills from unstructured text.
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Optional, Set, Tuple


DEFAULT_SKILLS_TAXONOMY: Dict[str, Dict[str, List[str]]] = {
    "categories": {
        "Programming Languages": [
            "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "golang", 
            "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "matlab", "shell", "bash", "powershell", "sql", "html", "css"
        ],
        "AI, ML & Data Science": [
            "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
            "large language models", "llm", "generative ai", "genai", "prompt engineering", "langchain",
            "transformers", "hugging face", "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn",
            "pandas", "numpy", "scipy", "xgboost", "lightgbm", "catboost", "opencv", "spacy", "nltk",
            "bert", "gpt", "rag", "retrieval augmented generation", "vector databases", "faiss", "chromadb",
            "pinecone", "qdrant", "reinforcement learning", "supervised learning", "unsupervised learning",
            "feature engineering", "model deployment", "mlops", "data analysis", "data visualization",
            "matplotlib", "seaborn", "plotly", "bi tools", "tableau", "power bi", "dbt", "spark", "pyspark"
        ],
        "Web & App Frameworks": [
            "react", "react.js", "next.js", "nextjs", "vue", "vue.js", "angular", "svelte", "node.js", "nodejs",
            "express", "express.js", "django", "flask", "fastapi", "spring boot", "spring", "asp.net", ".net",
            "laravel", "ruby on rails", "flutter", "react native", "tailwind", "tailwind css", "bootstrap",
            "graphql", "rest api", "restful apis", "websockets", "microservices"
        ],
        "Cloud & DevOps": [
            "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes", "k8s",
            "terraform", "ansible", "ci/cd", "continuous integration", "github actions", "gitlab ci",
            "jenkins", "helm", "prometheus", "grafana", "linux", "nginx", "apache", "serverless", "lambda"
        ],
        "Databases & Storage": [
            "postgresql", "postgres", "mysql", "mongodb", "sqlite", "redis", "elasticsearch", "cassandra",
            "dynamodb", "snowflake", "bigquery", "redshift", "firebase", "firestore", "supabase", "neo4j",
            "mariadb", "oracle db"
        ],
        "Software Engineering & Tools": [
            "git", "github", "gitlab", "bitbucket", "jira", "confluence", "agile", "scrum", "kanban",
            "unit testing", "test driven development", "tdd", "integration testing", "pytest", "jest",
            "postman", "selenium", "cypress", "system design", "object oriented programming", "oop",
            "design patterns", "data structures", "algorithms"
        ],
        "Soft Skills & Leadership": [
            "problem solving", "communication", "team collaboration", "leadership", "critical thinking",
            "project management", "time management", "adaptability", "stakeholder management", "mentorship",
            "analytical skills", "cross-functional collaboration", "presentation skills", "conflict resolution"
        ],
        "Certifications & Education": [
            "aws certified", "azure certified", "gcp professional", "pmp", "scrum master", "csm",
            "cissp", "ceh", "b.tech", "b.e", "m.tech", "m.s", "computer science", "artificial intelligence", "data science"
        ]
    },
    "aliases": {
        "js": "javascript",
        "ts": "typescript",
        "py": "python",
        "k8s": "kubernetes",
        "tf": "tensorflow",
        "reactjs": "react",
        "react.js": "react",
        "nextjs": "next.js",
        "vuejs": "vue",
        "vue.js": "vue",
        "nodejs": "node.js",
        "expressjs": "express",
        "express.js": "express",
        "postgres": "postgresql",
        "sklearn": "scikit-learn",
        "amazon web services": "aws",
        "google cloud platform": "gcp",
        "google cloud": "gcp",
        "microsoft azure": "azure",
        "natural language processing": "nlp",
        "large language models": "llm",
        "retrieval augmented generation": "rag",
        "continuous integration": "ci/cd",
        "ci/cd pipeline": "ci/cd",
        "test driven development": "tdd",
        "object oriented programming": "oop"
    }
}


class SkillExtractor:
    """Extracts and standardizes technical and professional skills from text."""

    def __init__(self, taxonomy_file_path: Optional[str] = None):
        self.taxonomy: Dict[str, Dict[str, List[str]]] = DEFAULT_SKILLS_TAXONOMY
        if taxonomy_file_path and os.path.exists(taxonomy_file_path):
            try:
                with open(taxonomy_file_path, "r", encoding="utf-8") as f:
                    self.taxonomy = json.load(f)
            except Exception:
                self.taxonomy = DEFAULT_SKILLS_TAXONOMY

        self.categories: Dict[str, List[str]] = self.taxonomy.get("categories", {})
        self.aliases: Dict[str, str] = self.taxonomy.get("aliases", {})
        
        # Build reverse mapping from skill/variant to category
        self.skill_to_category: Dict[str, str] = {}
        self.all_skill_phrases: List[str] = []
        
        for category, skill_list in self.categories.items():
            for skill in skill_list:
                norm = skill.strip().lower()
                self.skill_to_category[norm] = category
                self.all_skill_phrases.append(norm)

        for alias, canon in self.aliases.items():
            alias_norm = alias.strip().lower()
            canon_norm = canon.strip().lower()
            if canon_norm in self.skill_to_category:
                self.skill_to_category[alias_norm] = self.skill_to_category[canon_norm]
            self.all_skill_phrases.append(alias_norm)

        # Sort longest phrase first so multi-word matches take precedence
        self.all_skill_phrases = sorted(list(set(self.all_skill_phrases)), key=lambda s: len(s), reverse=True)

    def normalize_skill(self, skill: str) -> str:
        """Resolve skill aliases to their canonical representation."""
        norm = skill.strip().lower()
        return self.aliases.get(norm, norm)

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """Extract all recognized skills from input text with categories and counts."""
        if not text:
            return {"skills": [], "by_category": {}, "total_count": 0}

        lowered_text = text.lower()
        found_canonical: Set[str] = set()
        skill_counts: Dict[str, int] = {}

        for skill_phrase in self.all_skill_phrases:
            # Special regex boundary handling for symbols like c++, c#, .net, r, c
            if skill_phrase in {"c++", "c#", ".net"}:
                pattern = rf"(?<![\w#+]){re.escape(skill_phrase)}(?![\w#+])"
            elif skill_phrase in {"c", "r"}:
                # Avoid matching single letters inside normal words; require explicit tech context
                pattern = rf"\b(?:language\s+)?{skill_phrase}\b(?:\s+(?:programming|language|developer))?"
            else:
                pattern = rf"\b{re.escape(skill_phrase)}\b"

            matches = list(re.finditer(pattern, lowered_text))
            if matches:
                canonical = self.normalize_skill(skill_phrase)
                found_canonical.add(canonical)
                skill_counts[canonical] = skill_counts.get(canonical, 0) + len(matches)

        # Categorize detected skills
        by_category: Dict[str, List[str]] = {cat: [] for cat in self.categories}
        for skill in sorted(found_canonical):
            category = self.skill_to_category.get(skill, "Other Technical Skills")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill.title() if len(skill) > 4 else skill.upper())

        # Clean empty categories
        by_category = {cat: skills for cat, skills in by_category.items() if skills}

        return {
            "skills": sorted(list(found_canonical)),
            "by_category": by_category,
            "skill_counts": skill_counts,
            "total_count": len(found_canonical)
        }
