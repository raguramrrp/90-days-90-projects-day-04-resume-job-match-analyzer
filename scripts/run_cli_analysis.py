"""Command-Line Interface (CLI) for Resume-Job Description Match Analysis.

Usage:
    python scripts/run_cli_analysis.py --resume data/sample_resumes/alex_chen_data_scientist.txt --jd data/sample_jds/ai_data_scientist_job_description.txt
"""

import argparse
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser import extract_text_from_file, extract_contact_info, extract_sections
from src.skill_extractor import SkillExtractor
from src.matcher import CompatibilityMatcher
from src.ats_analyzer import ATSAnalyzer
from src.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="AI Resume-Job Compatibility Analyzer CLI")
    parser.add_argument("--resume", required=True, help="Path to resume file (.pdf, .docx, .txt)")
    parser.add_argument("--jd", required=True, help="Path to job description file (.txt, .pdf, .docx)")
    parser.add_argument("--export-html", default=None, help="Optional output path for HTML scorecard")
    parser.add_argument("--export-json", default=None, help="Optional output path for JSON report")

    args = parser.parse_args()

    if not os.path.exists(args.resume):
        print(f"[ERROR] Resume file not found: {args.resume}")
        sys.exit(1)

    if not os.path.exists(args.jd):
        print(f"[ERROR] Job description file not found: {args.jd}")
        sys.exit(1)

    # Read and parse files
    with open(args.resume, "rb") as f:
        resume_bytes = f.read()
    with open(args.jd, "rb") as f:
        jd_bytes = f.read()

    print("[*] Parsing documents...")
    resume_text = extract_text_from_file(resume_bytes, os.path.basename(args.resume))
    jd_text = extract_text_from_file(jd_bytes, os.path.basename(args.jd))

    sections = extract_sections(resume_text)
    contacts = extract_contact_info(resume_text)

    # Initialize NLP engines
    taxonomy_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "skills_taxonomy.json")
    extractor = SkillExtractor(taxonomy_file_path=taxonomy_path)
    matcher = CompatibilityMatcher(skill_extractor=extractor)
    analyzer = ATSAnalyzer()

    print("[*] Running ATS compatibility analysis...")
    ats_health = analyzer.analyze_resume(resume_text, sections, contacts)
    match_result = matcher.match(
        resume_text, 
        jd_text, 
        section_score=ats_health["section_score"],
        verb_impact_score=ats_health["verb_impact_score"]
    )
    recommendations = analyzer.generate_recommendations(match_result, ats_health)

    print("\n" + "="*70)
    print("   AI-POWERED RESUME–JOB COMPATIBILITY REPORT")
    print("="*70)
    print(f"Overall ATS Score       : {match_result['overall_score']}% [{match_result['tier']}]")
    print(f"Skill Coverage Score    : {match_result['skill_coverage_score']}% ({match_result['matched_skills_count']}/{match_result['total_jd_skills_count']} skills)")
    print(f"Semantic TF-IDF Fit     : {match_result['tfidf_similarity']}%")
    print(f"Action & Impact Score   : {ats_health['verb_impact_score']}% ({ats_health['metric_count']} metrics, {ats_health['strong_verbs_count']} power verbs)")
    print(f"Section Completeness    : {ats_health['section_score']}%")
    print("-"*70)

    print(f"\n[+] Matched Skills ({len(match_result['matched_skills'])}):")
    print("    " + ", ".join(match_result['matched_skills'][:15]))

    high_missing = match_result['missing_skills_by_priority']['high']
    if high_missing:
        print(f"\n[!] HIGH-PRIORITY Missing Skills ({len(high_missing)}):")
        print("    " + ", ".join(high_missing))

    med_missing = match_result['missing_skills_by_priority']['medium']
    if med_missing:
        print(f"\n[-] Medium-Priority Missing Skills ({len(med_missing)}):")
        print("    " + ", ".join(med_missing))

    print("\n[+] Top Actionable ATS Recommendations:")
    for idx, rec in enumerate(recommendations[:4], 1):
        print(f"    {idx}. [{rec['priority']}] {rec['title']}")
        print(f"       -> Action: {rec['action']}")

    # Export if requested
    if args.export_html:
        html_out = ReportGenerator.generate_html_report(match_result, ats_health, recommendations)
        with open(args.export_html, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"\n[SAVED] HTML Scorecard written to: {args.export_html}")

    if args.export_json:
        json_out = ReportGenerator.generate_json_report(match_result, ats_health, recommendations)
        with open(args.export_json, "w", encoding="utf-8") as f:
            f.write(json_out)
        print(f"[SAVED] JSON Report written to: {args.export_json}")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
