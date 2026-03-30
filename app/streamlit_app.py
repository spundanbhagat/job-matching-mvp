import streamlit as st

st.set_page_config(
    page_title="AI Job Matching & Skills Gap Planner",
    page_icon="",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.hero-card {
    padding: 1.4rem 1.2rem;
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 16px;
    background: rgba(255,255,255,0.02);
    margin-bottom: 1rem;
}
.info-card {
    padding: 1rem;
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 14px;
    background: rgba(255,255,255,0.02);
    height: 100%;
}
.small-muted {
    font-size: 0.92rem;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Job Matching & Skills Gap Planner")
st.caption("A prototype for workforce programs: candidate guidance + admin analytics")

st.markdown("""
<div class="hero-card">
    <h3 style="margin-top:0;">What this MVP does</h3>
    <p class="small-muted">
        Match candidates to jobs, explain the fit, identify missing skills, recommend a learning path,
        and help program teams monitor funnel performance and skill-gap trends.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4 style="margin-top:0;">Candidate App</h4>
        <p class="small-muted">
            Explore candidate-job matching, missing skills, course recommendations, and learning paths.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_candidate_app.py", label="Open Candidate App", icon="👤")

with col2:
    st.markdown("""
    <div class="info-card">
        <h4 style="margin-top:0;">Admin Dashboard</h4>
        <p class="small-muted">
            Monitor applications, funnel stages, top job categories, and the most common missing skills.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_admin_dashboard.py", label="Open Admin Dashboard", icon="📊")