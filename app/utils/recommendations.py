from __future__ import annotations

import pandas as pd
from typing import List, Dict


def recommend_courses_for_skills(
    missing_skills: List[str],
    courses_df: pd.DataFrame,
    max_recommendations: int = 5
) -> List[Dict]:
    """
    Return up to max_recommendations courses covering missing skills.
    """
    if not missing_skills:
        return []

    df = courses_df.copy()
    df["skill_covered_norm"] = df["skill_covered"].astype(str).str.strip().str.lower()

    missing_norm = [skill.strip().lower() for skill in missing_skills]

    filtered = df[df["skill_covered_norm"].isin(missing_norm)].copy()

    if filtered.empty:
        return []

    filtered = filtered.drop_duplicates(subset=["skill_covered_norm"])
    filtered = filtered.head(max_recommendations)

    return filtered[
        [
            "course_id",
            "course_name",
            "provider",
            "skill_covered",
            "duration_weeks",
            "difficulty",
            "course_type",
        ]
    ].to_dict(orient="records")


def build_learning_path(
    missing_skills: List[str],
    courses_df: pd.DataFrame
) -> List[str]:
    """
    Return simple learning path steps as readable text.
    """
    course_recs = recommend_courses_for_skills(missing_skills, courses_df)

    steps = []
    for i, course in enumerate(course_recs, start=1):
        steps.append(
            f"Step {i}: Learn {course['skill_covered']} via {course['course_name']} "
            f"({course['provider']}, {course['duration_weeks']} weeks)"
        )

    return steps