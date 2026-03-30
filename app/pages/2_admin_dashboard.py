from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.preprocessing import load_skills_lookup, standardize_skills_column
from utils.matching import compute_skill_match


st.markdown("""
<style>
.section-card {
    padding: 1rem 1rem 0.9rem 1rem;
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 16px;
    background: rgba(255,255,255,0.02);
    margin-bottom: 1rem;
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
    applications_df = pd.read_csv("data/applications.csv")

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

    applications_df["application_status"] = applications_df["application_status"].astype(str).str.strip()
    applications_df["status_date"] = pd.to_datetime(applications_df["status_date"], errors="coerce")

    return candidates_df, jobs_df, courses_df, applications_df


def build_application_analysis(applications_df: pd.DataFrame,
                               candidates_df: pd.DataFrame,
                               jobs_df: pd.DataFrame) -> pd.DataFrame:
    merged = applications_df.merge(
        candidates_df[["candidate_id", "full_name", "location", "desired_job_category", "skills_list_std"]],
        on="candidate_id",
        how="left"
    ).merge(
        jobs_df[["job_id", "title", "category", "location", "work_mode", "required_skills_std"]],
        on="job_id",
        how="left",
        suffixes=("_candidate", "_job")
    )

    matched_skills_list = []
    missing_skills_list = []
    missing_count_list = []

    for _, row in merged.iterrows():
        candidate_skills = row["skills_list_std"] if isinstance(row["skills_list_std"], list) else []
        job_skills = row["required_skills_std"] if isinstance(row["required_skills_std"], list) else []

        result = compute_skill_match(candidate_skills, job_skills)

        matched_skills_list.append(result["matched_skills"])
        missing_skills_list.append(result["missing_skills"])
        missing_count_list.append(len(result["missing_skills"]))

    merged["matched_skills"] = matched_skills_list
    merged["missing_skills"] = missing_skills_list
    merged["missing_skills_count"] = missing_count_list

    return merged


candidates_df, jobs_df, courses_df, applications_df = load_data()
analysis_df = build_application_analysis(applications_df, candidates_df, jobs_df)

st.title("📊 Admin / Operations Dashboard")
st.caption("Track funnel performance, skill gaps, and job-category demand.")

st.sidebar.header("Filters")

location_options = ["All"] + sorted(analysis_df["location_candidate"].dropna().unique().tolist())
category_options = ["All"] + sorted(analysis_df["category"].dropna().unique().tolist())
status_options = sorted(analysis_df["application_status"].dropna().unique().tolist())

selected_location = st.sidebar.selectbox("Candidate Location", location_options)
selected_category = st.sidebar.selectbox("Job Category", category_options)
selected_statuses = st.sidebar.multiselect("Application Status", status_options, default=status_options)

filtered_df = analysis_df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location_candidate"] == selected_location]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

filtered_df = filtered_df[filtered_df["application_status"].isin(selected_statuses)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

stage_counts = filtered_df["application_status"].value_counts()

total_candidates = filtered_df["candidate_id"].nunique()
total_applications = filtered_df["application_id"].nunique()
avg_match_score = round(filtered_df["match_score"].mean(), 1)
avg_missing_skills = round(filtered_df["missing_skills_count"].mean(), 1)

applied_plus = int(
    stage_counts.get("Applied", 0)
    + stage_counts.get("Interviewed", 0)
    + stage_counts.get("Placed", 0)
    + stage_counts.get("Rejected", 0)
)
interviewed_plus = int(
    stage_counts.get("Interviewed", 0)
    + stage_counts.get("Placed", 0)
)
placed_count = int(stage_counts.get("Placed", 0))

match_to_application_conversion = round((applied_plus / total_applications) * 100, 1) if total_applications else 0.0
application_to_interview_conversion = round((interviewed_plus / applied_plus) * 100, 1) if applied_plus else 0.0
interview_to_placement_conversion = round((placed_count / interviewed_plus) * 100, 1) if interviewed_plus else 0.0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Candidates", total_candidates)
m2.metric("Applications", total_applications)
m3.metric("Avg Match Score", f"{avg_match_score}%")
m4.metric("Avg Missing Skills", avg_missing_skills)

m5, m6, m7 = st.columns(3)
m5.metric("Match → Application", f"{match_to_application_conversion}%")
m6.metric("Application → Interview", f"{application_to_interview_conversion}%")
m7.metric("Interview → Placement", f"{interview_to_placement_conversion}%")

tab1, tab2, tab3 = st.tabs(["Overview", "Skill Gaps", "Detailed View"])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        funnel_order = ["Matched", "Applied", "Interviewed", "Placed", "Rejected"]
        funnel_df = (
            filtered_df["application_status"]
            .value_counts()
            .reindex(funnel_order, fill_value=0)
            .reset_index()
        )
        funnel_df.columns = ["Stage", "Count"]

        fig_funnel = px.bar(
            funnel_df,
            x="Stage",
            y="Count",
            title="Application Funnel"
        )
        fig_funnel.update_layout(height=400)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with c2:
        category_df = (
            filtered_df.groupby("category")["application_id"]
            .count()
            .reset_index(name="Applications")
            .sort_values(by="Applications", ascending=False)
        )

        fig_category = px.bar(
            category_df,
            x="category",
            y="Applications",
            title="Applications by Job Category"
        )
        fig_category.update_layout(height=400, xaxis_title="Job Category")
        st.plotly_chart(fig_category, use_container_width=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Operational Summary")
    st.markdown(
        f"""
        <div class="muted">
            This filtered view covers <b>{total_candidates}</b> unique candidates and <b>{total_applications}</b> application records.
            Average match quality is <b>{avg_match_score}%</b>, and candidates are missing an average of
            <b>{avg_missing_skills}</b> required skills per application.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    exploded_skills_df = filtered_df.explode("missing_skills").copy()
    exploded_skills_df["missing_skills"] = exploded_skills_df["missing_skills"].astype(str).str.strip()
    exploded_skills_df = exploded_skills_df[
        exploded_skills_df["missing_skills"].notna()
        & (exploded_skills_df["missing_skills"] != "")
        & (exploded_skills_df["missing_skills"] != "nan")
        & (exploded_skills_df["missing_skills"] != "[]")
    ]

    if exploded_skills_df.empty:
        st.info("No missing skills found for the current filters.")
    else:
        s1, s2 = st.columns([2, 1])

        with s1:
            missing_skills_df = (
                exploded_skills_df.groupby("missing_skills")["application_id"]
                .count()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .head(12)
            )

            fig_missing = px.bar(
                missing_skills_df,
                x="missing_skills",
                y="Count",
                title="Top Missing Skills"
            )
            fig_missing.update_layout(height=420, xaxis_title="Skill")
            st.plotly_chart(fig_missing, use_container_width=True)

        with s2:
            category_gap_df = (
                filtered_df.groupby("category")["missing_skills_count"]
                .mean()
                .reset_index(name="Avg Missing Skills")
                .sort_values(by="Avg Missing Skills", ascending=False)
            )
            st.markdown("### Gap Severity by Category")
            st.dataframe(category_gap_df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Application Detail Table")

    display_df = filtered_df[
        [
            "application_id",
            "status_date",
            "full_name",
            "title",
            "category",
            "location_candidate",
            "work_mode",
            "match_score",
            "application_status",
            "missing_skills_count",
            "missing_skills",
        ]
    ].copy()

    display_df = display_df.rename(columns={
        "full_name": "Candidate",
        "title": "Job Title",
        "category": "Job Category",
        "location_candidate": "Candidate Location",
        "work_mode": "Work Mode",
        "match_score": "Match Score",
        "application_status": "Status",
        "missing_skills_count": "Missing Skills Count",
        "missing_skills": "Missing Skills",
        "status_date": "Status Date",
    })

    display_df = display_df.sort_values(by="Status Date", ascending=False)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered application data",
        data=csv_data,
        file_name="filtered_applications.csv",
        mime="text/csv"
    )