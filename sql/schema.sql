-- AI Job Matching & Skills Gap Planner
-- MVP relational schema


CREATE TABLE skills_taxonomy (
    skill_id VARCHAR(10) PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    skill_category VARCHAR(100),
    aliases TEXT
);

CREATE TABLE candidates (
    candidate_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    location VARCHAR(100),
    education_level VARCHAR(50),
    years_experience DECIMAL(4,1) DEFAULT 0,
    desired_job_category VARCHAR(100),
    skills_list TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    job_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    work_mode VARCHAR(50),
    min_experience DECIMAL(4,1) DEFAULT 0,
    education_required VARCHAR(50),
    required_skills TEXT NOT NULL,
    preferred_skills TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    provider VARCHAR(100),
    skill_covered VARCHAR(100) NOT NULL,
    duration_weeks INTEGER,
    difficulty VARCHAR(50),
    course_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    application_id VARCHAR(10) PRIMARY KEY,
    candidate_id VARCHAR(10) NOT NULL,
    job_id VARCHAR(10) NOT NULL,
    match_score DECIMAL(5,2),
    application_status VARCHAR(50) NOT NULL,
    status_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_app_candidate
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    CONSTRAINT fk_app_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE INDEX idx_candidates_location ON candidates(location);
CREATE INDEX idx_candidates_desired_job_category ON candidates(desired_job_category);

CREATE INDEX idx_jobs_category ON jobs(category);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_is_active ON jobs(is_active);

CREATE INDEX idx_courses_skill_covered ON courses(skill_covered);

CREATE INDEX idx_applications_candidate_id ON applications(candidate_id);
CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_applications_status ON applications(application_status);
CREATE INDEX idx_applications_status_date ON applications(status_date);

-- Optional analytics view for quick admin reporting
CREATE VIEW application_summary AS
SELECT
    a.application_id,
    a.candidate_id,
    c.full_name,
    c.location AS candidate_location,
    c.education_level,
    c.years_experience,
    c.desired_job_category,
    a.job_id,
    j.title AS job_title,
    j.category AS job_category,
    j.location AS job_location,
    a.match_score,
    a.application_status,
    a.status_date
FROM applications a
JOIN candidates c ON a.candidate_id = c.candidate_id
JOIN jobs j ON a.job_id = j.job_id;