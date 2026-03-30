# KPI Definitions
## AI Job Matching & Skills Gap Planner

---

## 1. Purpose
This document defines the key product and program metrics for the AI Job Matching & Skills Gap Planner MVP.

The goal is to measure two things:

1. **candidate value**
   - whether users receive useful job-match and skills-gap guidance

2. **program value**
   - whether admins can monitor and improve employment outcomes

These KPIs are intentionally practical and MVP-friendly. They are not meant to represent full production analytics maturity.

---

## 2. KPI Design Principles
All KPIs in this document should be:
- clearly defined
- measurable from available data
- tied to a user or business outcome
- understandable by non-technical stakeholders

Avoid vanity metrics unless they support a real decision.

---

# Candidate-Side KPIs

## 3. Match Result View Rate

### Definition
The percentage of candidate sessions in which job match results are successfully viewed after profile input.

### Formula
`Match Result View Rate = (Number of sessions that reached match results / Number of profile submission sessions) × 100`

### Why it matters
This measures whether users are successfully reaching the core value moment of the product.

### Owner
Product / UX

### Frequency
Weekly

### Caveat
A high value does not mean the recommendations are useful. It only means users reached the results page.

---

## 4. Recommendation Engagement Rate

### Definition
The percentage of match-result sessions in which users interact with learning recommendations.

### Formula
`Recommendation Engagement Rate = (Number of sessions with course/recommendation interaction / Number of sessions that viewed match results) × 100`

### Why it matters
This shows whether users find the skill-gap output actionable enough to explore learning options.

### Owner
Product

### Frequency
Weekly

### Caveat
In the MVP prototype, this may need to be approximated if click tracking is not fully implemented.

---

## 5. Average Match Score

### Definition
The average job-match score across candidate-job matches or applications.

### Formula
`Average Match Score = Sum of match scores / Total number of matches`

### Why it matters
This gives a directional view of how strong the average recommendation quality is.

### Owner
Product / Analytics

### Frequency
Weekly

### Caveat
This is only meaningful if the scoring logic is consistent and reasonably calibrated.

---

## 6. Average Missing Skills Count

### Definition
The average number of required skills missing from candidate-job matches.

### Formula
`Average Missing Skills Count = Total missing skills across matches / Total number of matches`

### Why it matters
This indicates how far candidates are from job readiness on average.

### Owner
Program Operations

### Frequency
Weekly

### Caveat
This metric can look artificially high or low depending on how detailed job requirements are.

---

## 7. Apply-Intent Proxy Rate

### Definition
The percentage of matched candidates who proceed to an apply stage or a strong equivalent signal.

### Formula
`Apply-Intent Proxy Rate = (Number of matched candidates who apply / Number of matched candidates) × 100`

### Why it matters
This is one of the clearest indicators that the recommendation output is useful enough to trigger action.

### Owner
Product / Program Operations

### Frequency
Weekly

### Caveat
A candidate may apply for reasons unrelated to recommendation quality.

---

# Admin / Program KPIs

## 8. Total Candidates

### Definition
The total number of unique candidates present in the system or filtered dataset.

### Formula
`Total Candidates = Count of unique candidate_id`

### Why it matters
This provides basic program scale visibility.

### Owner
Program Operations

### Frequency
Daily / Weekly

### Caveat
This is a volume metric, not a success metric.

---

## 9. Total Applications

### Definition
The total number of application records in the dataset or filtered view.

### Formula
`Total Applications = Count of application_id`

### Why it matters
This reflects throughput and program activity.

### Owner
Program Operations

### Frequency
Daily / Weekly

### Caveat
Multiple applications from the same candidate can inflate this number.

---

## 10. Match-to-Application Conversion Rate

### Definition
The percentage of matched candidates or matched records that progress to application.

### Formula
`Match-to-Application Conversion = (Applications / Matched records) × 100`

### Why it matters
This is a core signal of whether the recommended jobs feel relevant enough to act on.

### Owner
Product / Operations

### Frequency
Weekly

### Caveat
In a snapshot-based MVP dataset, this may be inferred from current statuses rather than event history.

---

## 11. Application-to-Interview Conversion Rate

### Definition
The percentage of applications that progress to interview.

### Formula
`Application-to-Interview Conversion = (Interviewed records / Applied records) × 100`

### Why it matters
This helps measure candidate quality and alignment between candidate profile and role requirements.

### Owner
Program Operations

### Frequency
Weekly / Monthly

### Caveat
This can also be influenced by employer-side demand and hiring capacity.

---

## 12. Interview-to-Placement Conversion Rate

### Definition
The percentage of interviewed candidates who are eventually placed.

### Formula
`Interview-to-Placement Conversion = (Placed records / Interviewed records) × 100`

### Why it matters
This reflects downstream program effectiveness and employer-fit quality.

### Owner
Program Operations / Leadership

### Frequency
Monthly

### Caveat
This metric is often slower-moving and may require longer observation windows.

---

## 13. Placement Rate

### Definition
The percentage of total applications or total candidates that result in placement.

### Formula
Option A:  
`Placement Rate = (Placed records / Total applications) × 100`

Option B:  
`Placement Rate = (Unique placed candidates / Total candidates) × 100`

### Why it matters
This is one of the clearest top-line indicators of program success.

### Owner
Leadership / Program Management

### Frequency
Monthly

### Caveat
You must state clearly which denominator is being used, or the metric becomes misleading.

---

## 14. Top Missing Skills by Frequency

### Definition
The most frequently occurring missing skills across candidate-job comparisons.

### Formula
`Top Missing Skills = Ranked count of missing skill occurrences`

### Why it matters
This supports training design, curriculum prioritization, and intervention planning.

### Owner
Program Operations / Learning & Development

### Frequency
Weekly / Monthly

### Caveat
This is descriptive, not causal. A frequent gap does not automatically mean it is the highest-impact gap.

---

## 15. Top Job Categories by Application Volume

### Definition
The job categories with the highest number of applications or matches.

### Formula
`Top Job Categories = Ranked count of applications grouped by job category`

### Why it matters
This helps admins understand demand concentration and program focus areas.

### Owner
Program Operations

### Frequency
Weekly

### Caveat
High volume does not necessarily mean high success or high placement quality.

---

## 16. Drop-off by Funnel Stage

### Definition
The number or share of candidates/applications that fail to progress at each stage of the funnel.

### Formula
`Drop-off at Stage X = Count entering stage X - Count progressing beyond stage X`

### Why it matters
This helps identify bottlenecks and where interventions are needed.

### Owner
Operations / Product

### Frequency
Weekly

### Caveat
A snapshot dataset gives weaker funnel truth than event-level stage history.

---

# Operational Notes

## 17. Metric Segmentation
Where possible, KPIs should be segmented by:
- location
- job category
- education level
- experience band
- cohort/program type

This makes the dashboard useful for intervention, not just reporting.

---

## 18. MVP Data Limitations
The MVP currently uses synthetic and snapshot-style data. That means:

- stage progression is simplified
- user behavior analytics may be partially simulated
- some KPIs are directional rather than production-grade

This is acceptable for a portfolio prototype, but it should be stated clearly.

---

## 19. North Star Metric
For the MVP, the best North Star metric is:

**Match-to-Application Conversion Rate**

### Why
Because it sits closest to the core promise of the product:
- recommend relevant jobs
- generate enough trust and value for a candidate to act

It is stronger than a pure view metric and earlier than final placement, which is slower and influenced by external factors.

---

## 20. Summary
These KPI definitions ensure the product is evaluated on actual usefulness, not just interface activity.

The KPI framework supports:
- candidate usefulness
- program efficiency
- operational bottleneck detection
- skill-gap intervention planning

That is what makes this prototype look like a real workforce-product concept rather than a generic dashboard demo.