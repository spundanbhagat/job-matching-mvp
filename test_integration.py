import pandas as pd

from app.utils.preprocessing import load_skills_lookup, standardize_skills_column
from app.utils.matching import get_top_job_matches
from app.utils.recommendations import recommend_courses_for_skills, build_learning_path

print("Loading datasets...")

candidates_df = pd.read_csv("data/candidates.csv")
jobs_df = pd.read_csv("data/jobs.csv")
skills_df = pd.read_csv("data/skills_taxonomy.csv")
courses_df = pd.read_csv("data/courses.csv")

print("Building skills alias lookup...")
alias_lookup = load_skills_lookup(skills_df)

print("Standardizing candidate skills...")
candidates_df = standardize_skills_column(
    candidates_df,
    source_col="skills_list",
    target_col="skills_list_std",
    alias_lookup=alias_lookup
)

print("Standardizing job required skills...")
jobs_df = standardize_skills_column(
    jobs_df,
    source_col="required_skills",
    target_col="required_skills_std",
    alias_lookup=alias_lookup
)

print("\nUsing first candidate for test...\n")
candidate = candidates_df.iloc[0]

print("Candidate selected:")
print(candidate[["candidate_id", "full_name", "desired_job_category", "skills_list_std"]])

print("\nComputing top job matches...\n")
matches = get_top_job_matches(candidate, jobs_df, top_n=5)

print(matches[["job_id", "job_title", "match_score", "matched_skills", "missing_skills", "explanation"]])

top_missing_skills = matches.iloc[0]["missing_skills"]

print("\nMissing skills for top match:")
print(top_missing_skills)

print("\nRecommended courses:")
course_recs = recommend_courses_for_skills(top_missing_skills, courses_df)
for course in course_recs:
    print(course)

print("\nLearning path:")
learning_path = build_learning_path(top_missing_skills, courses_df)
for step in learning_path:
    print(step)

print("\nIntegration test completed successfully.")