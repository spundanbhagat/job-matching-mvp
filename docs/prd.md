# Product Requirements Document (PRD)
## AI Job Matching & Skills Gap Planner

### 1. Overview
The AI Job Matching & Skills Gap Planner is a workforce-program prototype designed to help candidates identify suitable jobs, understand why they match, see which skills they are missing, and receive practical learning recommendations. It also provides program administrators with a dashboard to track placement funnel performance, common skill gaps, and job-category demand.

This product is intended for government workforce programs, skilling initiatives, employment support organizations, and similar public-sector or quasi-public-sector use cases.

---

### 2. Problem Statement
Workforce development programs often fail at the execution layer for three reasons:

1. **Job matching is opaque**  
   Candidates do not understand why a role is recommended or why they are not a fit.

2. **Skill gaps are not actionable**  
   Even when a gap is identified, users are rarely told what to learn next in a structured way.

3. **Program administrators lack operational visibility**  
   Teams cannot easily see where candidates are dropping off, which skills are most commonly missing, or which job categories are driving outcomes.

As a result, candidates receive low-value guidance, and admins struggle to improve program performance using data.

---

### 3. Goal
Build a working MVP that proves the following:

- candidates can be matched to relevant jobs using explainable logic
- missing skills can be identified clearly
- learning recommendations can be mapped to those missing skills
- admins can monitor program performance using funnel and skill-gap analytics

This is a product MVP, not a production hiring platform.

---

### 4. Target Users

#### 4.1 Candidate
A job seeker or program participant who wants to:
- upload or enter profile details
- discover suitable jobs
- understand match reasoning
- identify missing skills
- get learning recommendations

#### 4.2 Program Admin / Operations User
A workforce program manager, operations lead, or policy delivery team member who wants to:
- track candidate progress across the funnel
- understand common skill gaps
- monitor demand by job category
- evaluate conversion and placement outcomes

---

### 5. Primary Use Cases

#### Candidate Use Cases
- View top matched jobs based on profile and skills
- Understand why each job is a match
- Identify missing required skills for each role
- See recommended courses or learning actions

#### Admin Use Cases
- Monitor total candidates and total applications
- View funnel by stage: matched, applied, interviewed, placed, rejected
- Identify most common missing skills
- Track average match score and average missing skills
- See top job categories by application volume

---

### 6. Product Scope

#### In Scope (MVP)
- Candidate profile selection/input using structured data
- Rules-based job matching
- Match score display
- Match explanation display
- Missing skills detection
- Course recommendations based on missing skills
- Admin dashboard with operational analytics
- Synthetic dataset for demo and testing

#### Out of Scope (MVP)
- Real ATS integrations
- Employer portal
- Real CV parsing using OCR/LLMs
- Authentication and role-based access
- Multilingual support
- Live labor market APIs
- Personalized adaptive learning engine
- Production-grade deployment architecture

---

### 7. MVP Features

#### 7.1 Candidate App
The candidate-facing interface must allow a user to:
- select or input a candidate profile
- view standardized skills
- view top 5 job matches
- view match score for each job
- view explanation of match
- view missing skills
- view recommended courses
- view a simple learning path

#### 7.2 Admin Dashboard
The admin-facing interface must allow a user to:
- view total candidate count
- view total application count
- view average match score
- view average missing skills per application
- view conversion metrics across funnel stages
- view top job categories
- view top missing skills
- inspect a detailed application table

---

### 8. Functional Requirements

#### FR1. Candidate profile ingestion
The system shall load candidate profile data including:
- name
- location
- education level
- years of experience
- desired job category
- skills list

#### FR2. Skills standardization
The system shall standardize raw skill entries using a skills taxonomy and alias mapping.

#### FR3. Job matching
The system shall compute job-match scores using a weighted rules-based formula.

#### FR4. Match explanation
The system shall generate a plain-language explanation for each match using skill overlap and fit attributes.

#### FR5. Missing skills detection
The system shall identify required skills present in the job but absent in the candidate profile.

#### FR6. Course recommendation
The system shall map missing skills to relevant courses from the course dataset.

#### FR7. Admin analytics
The system shall generate aggregate operational views using applications, candidate, and job data.

---

### 9. Matching Logic

The MVP uses a rules-based scoring model rather than embeddings or advanced ML.

#### Proposed Weighting
- Skill overlap: 50%
- Experience fit: 20%
- Education fit: 10%
- Location fit: 10%
- Category preference fit: 10%

#### Example Formula
`match_score = 0.5 * skill_score + 0.2 * experience_score + 0.1 * education_score + 0.1 * location_score + 0.1 * preference_score`

#### Reason for this approach
This model is:
- explainable
- easy to validate
- easy to demo
- appropriate for MVP scope

Using complex ML at this stage would add technical noise without proving stronger product thinking.

---

### 10. Data Inputs

The MVP uses synthetic but realistic structured data:

- `candidates.csv`
- `jobs.csv`
- `skills_taxonomy.csv`
- `courses.csv`
- `applications.csv`

These datasets support:
- candidate matching
- skill normalization
- missing skill detection
- learning recommendations
- admin dashboard analytics

---

### 11. Success Metrics

#### Candidate Metrics
- Match result view rate
- Recommendation engagement rate
- Learning-path visibility rate
- Apply-intent proxy rate

#### Admin / Program Metrics
- Total candidates
- Total applications
- Match-to-application conversion
- Application-to-interview conversion
- Interview-to-placement conversion
- Average match score
- Average missing skills count
- Top missing skills by frequency

---

### 12. Assumptions
- Structured candidate and job data is available or can be simulated
- Skill aliases can be normalized into canonical terms
- A rules-based model is sufficient for MVP product proof
- Admin users care more about operational visibility than model complexity
- Course-to-skill mapping can be represented with simple structured data

---

### 13. Constraints
- No live external integrations in MVP
- No real resume parsing dependency
- No production auth or permissions
- No historical event-level funnel tracking beyond current application status snapshot
- Data quality is limited by synthetic dataset realism

---

### 14. Risks

#### Risk 1: Shallow matching quality
If the data is too simplistic, match outputs will look fake.

**Mitigation:**  
Use credible skill/job relationships and realistic skill distributions.

#### Risk 2: Weak admin value
If the dashboard is just charts without decisions, it will look cosmetic.

**Mitigation:**  
Focus on funnel, conversion, and top missing skills tied to intervention.

#### Risk 3: Overengineering
Adding embeddings, CV parsing, or chatbot features too early will slow delivery.

**Mitigation:**  
Keep v1 rules-based and transparent.

---

### 15. Release Definition for MVP
The MVP is considered complete when:

- candidate page shows top 5 job matches
- each match includes score, explanation, and missing skills
- course recommendations are generated for missing skills
- admin dashboard displays funnel, category demand, and skill-gap analytics
- datasets and utility modules run reliably end to end

---

### 16. Future Enhancements
Possible future versions may include:
- CV upload and structured parser
- semantic skill matching using embeddings
- employer-side job posting management
- cohort-level intervention recommendations
- multilingual candidate support
- role-based access and authentication
- API-backed architecture and database persistence

---

### 17. Summary
This MVP is designed to prove product judgment, not just coding ability. It demonstrates:
- clear user value
- scoped feature thinking
- transparent matching logic
- measurable admin analytics
- practical workforce-program relevance

The core strength of this product is that it connects candidate guidance with program-level decision support in one coherent workflow.