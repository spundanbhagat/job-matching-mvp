from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.preprocessing import load_skills_lookup, standardize_skills_column
from utils.matching import get_top_job_matches
from utils.recommendations import recommend_courses_for_skills, build_learning_path


st.markdown("""
<style>
.section-card {
    padding: 1rem 1rem 0.9rem 1rem;
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 16px;
    background: rgba(255,255,255,0.02);
    margin-bottom: 1rem;
}
.match-card {
    padding: 0.75rem 0.9rem;
    border: 1px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    background: rgba(255,255,255,0.02);
}
.kpi-label {
    font-size: 0.9rem;
    opacity: 0.8;
}
.kpi-value {
    font-size: 1.5rem;
    font-weight: 700;
}
.tag {
    display: inline-block;
    padding: 0.25rem 0.55rem;
    margin: 0.15rem 0.3rem 0.15rem 0;
    border-radius: 999px;
    font-size: 0.82rem;
    border: 1px solid rgba(128,128,128,0.25);
}
.tag-good {
    background: rgba(0, 200, 100, 0.12);
}
.tag-warn {
    background: rgba(255, 165, 0, 0.12);
}
.tag-neutral {
    background: rgba(120, 120, 120, 0.12);
}
.muted {
    opacity: 0.8;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    candidates_df = pd.read_csv("data/candidates.csv")
    jobs_df = pd.read_csv("data/jobs.csv")
    skills_df = pd.read_csv("data/skills_taxonomy.csv")
    courses_df = pd.read_csv("data/courses.csv")

    alias_lookup = load_skills_lookup(skills_df)

    candidates_df = standardize_skills_column(
        candidates_df,
        source_col="skills_list",
        target_col="skills_list_std",
        alias_lookup=alias_lookup
    )

    jobs_df = standardize_skills_column(
        jobs_df,
        source_col="required_skills",
        target_col="required_skills_std",
        alias_lookup=alias_lookup
    )

    return candidates_df, jobs_df, courses_df


def render_tags(items, tone="neutral"):
    if not items:
        return '<span class="tag tag-neutral">None</span>'

    cls = {
        "good": "tag tag-good",
        "warn": "tag tag-warn",
        "neutral": "tag tag-neutral"
    }.get(tone, "tag tag-neutral")

    return "".join([f'<span class="{cls}">{item}</span>' for item in items])


def score_label(score: float) -> str:
    if score >= 85:
        return "Strong fit"
    if score >= 70:
        return "Moderate fit"
    return "Weak fit"


candidates_df, jobs_df, courses_df = load_data()

st.title("👤 Candidate Job Matching")
st.caption("See top matches, why they fit, which skills are missing, and what to learn next.")

st.sidebar.header("Candidate Selection")
candidate_name = st.sidebar.selectbox(
    "Choose a candidate",
    candidates_df["full_name"].sort_values().tolist()
)

candidate = candidates_df[candidates_df["full_name"] == candidate_name].iloc[0]
matches_df = get_top_job_matches(candidate, jobs_df, top_n=5)

top_match_score = float(matches_df.iloc[0]["match_score"]) if not matches_df.empty else 0
avg_match_score = round(matches_df["match_score"].mean(), 1) if not matches_df.empty else 0
avg_missing_skills = round(matches_df["missing_skills"].apply(len).mean(), 1) if not matches_df.empty else 0
best_job = matches_df.iloc[0]["job_title"] if not matches_df.empty else "N/A"

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown("**Top Match Score**")
    st.markdown(f"### {top_match_score}%")

with metric2:
    st.markdown("**Best Match**")
    st.markdown(
        f"<div style='font-size:1.2rem; font-weight:700; line-height:1.3; word-wrap:break-word;'>{best_job}</div>",
        unsafe_allow_html=True
    )

with metric3:
    st.markdown("**Average Match Score**")
    st.markdown(f"### {avg_match_score}%")

with metric4:
    st.markdown("**Average Skill Gaps**")
    st.markdown(f"### {avg_missing_skills}")

left, right = st.columns([1, 2.4], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Profile Summary")
    st.write(f"**Name:** {candidate['full_name']}")
    st.write(f"**Location:** {candidate['location']}")
    st.write(f"**Education:** {candidate['education_level']}")
    st.write(f"**Experience:** {candidate['years_experience']} years")
    st.write(f"**Target Category:** {candidate['desired_job_category']}")
    st.markdown("**Skills**")
    st.markdown(render_tags(candidate["skills_list_std"], "neutral"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Readiness Snapshot")
    st.markdown(
        f"""
        <div class="muted">
            This candidate’s strongest current fit is <b>{best_job}</b> with a top score of <b>{top_match_score}%</b>.
            Use the match details to see whether the gap is small enough for direct application or requires targeted upskilling.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.subheader("Top 5 Job Matches")

    if matches_df.empty:
        st.warning("No job matches found.")
    else:
        for rank, (_, match) in enumerate(matches_df.iterrows(), start=1):
            job_detail = jobs_df[jobs_df["job_id"] == match["job_id"]].iloc[0]
            label = score_label(float(match["match_score"]))

            with st.expander(
    f"#{rank} {match['job_title']} | Score: {match['match_score']}% | {label}",
    expanded=(rank == 1)
):
                st.markdown('<div class="match-card">', unsafe_allow_html=True)

                c1, c2, c3 = st.columns([1.4, 1, 1])

                with c1:
                    st.markdown("**Category**")
                    st.write(match["job_category"])

                with c2:
                    st.markdown("**Location**")
                    st.write(match["job_location"])

                with c3:
                    st.markdown("**Work Mode**")
                    st.write(job_detail["work_mode"])

                st.progress(min(int(match["match_score"]), 100))
                st.caption(match["explanation"])

                st.markdown("**Role summary**")
                st.write(job_detail["description"])

                s1, s2 = st.columns(2)
                with s1:
                    st.markdown("**Matched Skills**")
                    st.markdown(render_tags(match["matched_skills"], "good"), unsafe_allow_html=True)

                with s2:
                    st.markdown("**Missing Skills**")
                    st.markdown(render_tags(match["missing_skills"], "warn"), unsafe_allow_html=True)

                tab1, tab2 = st.tabs(["Recommended Courses", "Learning Path"])

                with tab1:
                    course_recs = recommend_courses_for_skills(match["missing_skills"], courses_df)

                    if course_recs:
                        for course in course_recs:
                            st.markdown(
                                f"""
                                **{course['course_name']}**  
                                {course['provider']} · Skill: {course['skill_covered']} ·
                                {course['duration_weeks']} weeks · {course['difficulty']}
                                """
                            )
                    else:
                        st.success("No course recommendations needed. Candidate already covers required skills.")

                with tab2:
                    learning_steps = build_learning_path(match["missing_skills"], courses_df)

                    if learning_steps:
                        for i, step in enumerate(learning_steps, start=1):
                            st.write(f"{i}. {step}")
                    else:
                        st.success("No learning path required for core role eligibility.")

                st.markdown('</div>', unsafe_allow_html=True)