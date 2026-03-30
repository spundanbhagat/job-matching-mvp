# Job Matching & Skills Gap Planner

A prototype workforce-product MVP that matches candidates to relevant jobs, explains why they match, identifies missing skills, recommends learning paths, and gives program administrators an analytics dashboard to monitor placement funnel and skill gaps.

This project is designed for government workforce programs, skilling initiatives, employment support organizations, and public-sector SaaS use cases.

---

## Why this project exists

Most job-matching tools are weak in two places:

1. **candidate value is unclear**
   - users do not know why a role is recommended
   - users do not know which missing skills matter most
   - users do not know what to do next

2. **admin visibility is poor**
   - program teams cannot easily track funnel performance
   - common skill gaps are not visible
   - interventions are not data-driven

This prototype addresses both layers:
- **candidate guidance**
- **program intelligence**

---

## What the product does

### Candidate app
- loads a candidate profile
- standardizes skills using a skills taxonomy
- returns top 5 job matches
- shows match score
- explains why the role matched
- identifies missing skills
- recommends courses for missing skills
- builds a simple learning path

### Admin dashboard
- shows total candidates and applications
- shows average match score
- shows average missing skills
- visualizes placement funnel
- highlights top job categories
- highlights top missing skills
- provides a detailed application-level view

---

## Product objectives

This project is meant to prove the ability to:

- identify a real workforce problem
- scope a practical MVP
- define product requirements
- build explainable matching logic
- support product decisions with analytics
- connect user value with program-level outcomes

This is not a production hiring platform. It is a product proof prototype.

---

## Tech stack

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **CSV datasets**
- rules-based matching engine

Deliberately not used in v1:
- embeddings
- LLM-heavy parsing
- auth
- ATS integrations
- production deployment complexity

That is intentional. The goal is product clarity, not technical theater.

---

## Repository structure

```text
job-matching-mvp/
├── app/
│   ├── streamlit_app.py
│   ├── pages/
│   │   ├── 1_candidate_app.py
│   │   └── 2_admin_dashboard.py
│   ├── utils/
│   │   ├── matching.py
│   │   ├── preprocessing.py
│   │   └── recommendations.py
├── data/
│   ├── candidates.csv
│   ├── jobs.csv
│   ├── skills_taxonomy.csv
│   ├── courses.csv
│   └── applications.csv
├── notebooks/
│   └── synthetic_data_generator.ipynb
├── sql/
│   └── schema.sql
├── docs/
│   ├── prd.md
│   ├── personas.md
│   └── kpis.md
├── requirements.txt
└── README.md
Core datasets
candidates.csv

Contains:

candidate name

location

education

years of experience

desired job category

skills list

jobs.csv

Contains:

job title

category

location

work mode

minimum experience

education requirement

required skills

preferred skills

skills_taxonomy.csv

Contains:

canonical skill name

skill category

aliases used for standardization

courses.csv

Contains:

course name

provider

skill covered

duration

difficulty

applications.csv

Contains:

candidate-job application linkage

match score

application status

status date

Matching logic

This MVP uses a rules-based weighted scoring model.

Score components

Skill overlap — 50%

Experience fit — 20%

Education fit — 10%

Location fit — 10%

Category preference fit — 10%

Formula
match_score =
0.5 * skill_score +
0.2 * experience_score +
0.1 * education_score +
0.1 * location_score +
0.1 * preference_score
Why rules-based first

Because for an MVP:

it is explainable

it is easy to debug

it is easier to validate

it proves product thinking faster than black-box ML

Main modules
preprocessing.py

Responsible for:

building alias-to-skill lookup

normalizing raw skill text

standardizing skills into canonical format

matching.py

Responsible for:

skill overlap calculation

experience / education / location / preference scoring

total match score calculation

missing skills detection

plain-language explanation generation

recommendations.py

Responsible for:

mapping missing skills to courses

building a simple learning path

Setup instructions
1. Clone the repository
git clone <your-repo-url>
cd job-matching-mvp
2. Create virtual environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
Run the app

From the project root:

streamlit run app/streamlit_app.py

Make sure you run that command from the project root, not from inside the app/ folder.

Integration test

The project includes a simple end-to-end integration check through a standalone Python script.

What it validates

datasets load correctly

skill taxonomy standardization works

top job matches are returned

missing skills are identified

course recommendations are produced

Run the test
python test_integration.py

If imports fail or files are not found, the project is being run from the wrong directory or file paths are incorrect.

App walkthrough
Candidate page

The candidate page allows the user to:

select a candidate profile

view profile details

see top 5 matched jobs

inspect matched and missing skills

explore recommended courses

review a learning path

Admin dashboard

The admin dashboard allows the user to:

filter by candidate location and job category

view funnel metrics

monitor program conversion rates

inspect top missing skills

inspect job category demand

review a detailed application table

Documents included
docs/prd.md

Defines:

product problem

scope

requirements

goals

matching logic

MVP success definition

docs/personas.md

Defines:

candidate persona

reskilling persona

admin persona

stakeholder persona

docs/kpis.md

Defines:

candidate KPIs

admin/program KPIs

formulas

rationale

caveats

north star metric

Current MVP limitations

This prototype has real value, but it also has clear limitations.

Current limitations

uses synthetic datasets

applications data is snapshot-based, not full event history

matching logic is rules-based, not semantic

no real CV parser

no ATS or LMS integration

no authentication or permissions

no persistence layer beyond flat files

These are acceptable trade-offs for a portfolio MVP.

Future improvements

Logical next steps:

add manual candidate form input

add CV upload and parser

move data from CSV to SQL database

add event-level funnel tracking

introduce semantic skill matching

add employer-side job management

add cohort-based analytics

add intervention recommendations for admins
