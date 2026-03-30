from __future__ import annotations

import pandas as pd
from typing import Dict, List


def score_experience(candidate_years: float, required_years: float) -> float:
    if required_years <= 0:
        return 1.0
    if candidate_years >= required_years:
        return 1.0
    return round(candidate_years / required_years, 2)


def score_education(candidate_edu: str, required_edu: str) -> float:
    rank = {
        "high school": 1,
        "diploma": 2,
        "bachelor": 3,
        "master": 4,
        "phd": 5,
    }

    c = rank.get(str(candidate_edu).strip().lower(), 0)
    r = rank.get(str(required_edu).strip().lower(), 0)

    return 1.0 if c >= r else 0.0


def score_location(candidate_location: str, job_location: str) -> float:
    return 1.0 if str(candidate_location).strip().lower() == str(job_location).strip().lower() else 0.5


def score_preference(candidate_category: str, job_category: str) -> float:
    return 1.0 if str(candidate_category).strip().lower() == str(job_category).strip().lower() else 0.4


def compute_skill_match(candidate_skills: List[str], required_skills: List[str]) -> Dict:
    candidate_set = set([s.strip().lower() for s in candidate_skills])
    required_set = set([s.strip().lower() for s in required_skills])

    matched = sorted(candidate_set.intersection(required_set))
    missing = sorted(required_set.difference(candidate_set))

    skill_score = len(matched) / len(required_set) if required_set else 0.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score": round(skill_score, 2),
    }


def generate_match_explanation(
    matched_skills: List[str],
    exp_score: float,
    pref_score: float,
    loc_score: float
) -> str:
    reasons = []

    if matched_skills:
        reasons.append(f"strong skill overlap in {', '.join(matched_skills[:3])}")
    if exp_score >= 1.0:
        reasons.append("experience meets the role requirement")
    if pref_score >= 1.0:
        reasons.append("role aligns with preferred category")
    if loc_score >= 1.0:
        reasons.append("location is a direct fit")

    if not reasons:
        return "Partial match based on limited overlap."

    return "Matched because " + "; ".join(reasons) + "."


def score_candidate_to_job(candidate_row: pd.Series, job_row: pd.Series) -> Dict:
    candidate_skills = candidate_row["skills_list_std"]
    job_required_skills = job_row["required_skills_std"]

    skill_result = compute_skill_match(candidate_skills, job_required_skills)

    exp_score = score_experience(
        float(candidate_row["years_experience"]),
        float(job_row["min_experience"])
    )
    edu_score = score_education(
        candidate_row["education_level"],
        job_row["education_required"]
    )
    loc_score = score_location(
        candidate_row["location"],
        job_row["location"]
    )
    pref_score = score_preference(
        candidate_row["desired_job_category"],
        job_row["category"]
    )

    total_score = (
        0.5 * skill_result["skill_score"]
        + 0.2 * exp_score
        + 0.1 * edu_score
        + 0.1 * loc_score
        + 0.1 * pref_score
    ) * 100

    explanation = generate_match_explanation(
        matched_skills=skill_result["matched_skills"],
        exp_score=exp_score,
        pref_score=pref_score,
        loc_score=loc_score,
    )

    return {
        "job_id": job_row["job_id"],
        "job_title": job_row["title"],
        "job_category": job_row["category"],
        "job_location": job_row["location"],
        "match_score": round(total_score, 1),
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "explanation": explanation,
    }


def get_top_job_matches(
    candidate_row: pd.Series,
    jobs_df: pd.DataFrame,
    top_n: int = 5
) -> pd.DataFrame:
    results = []

    for _, job_row in jobs_df.iterrows():
        results.append(score_candidate_to_job(candidate_row, job_row))

    results_df = pd.DataFrame(results).sort_values(
        by="match_score",
        ascending=False
    ).head(top_n)

    return results_df.reset_index(drop=True)