# Create requirements.txt with all necessary dependencies
requirements_content = '''# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
jinja2==3.1.2

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
psycopg2-binary==2.9.9

# Redis & Caching
redis==5.0.1
hiredis==2.2.3

# Async Task Queue
celery==5.3.4
kombu==5.3.4
flower==2.0.1

# Machine Learning & NLP
torch==2.1.1
transformers==4.35.2
spacy==3.7.2
scikit-learn==1.3.2
numpy==1.25.2
pandas==2.1.4
nltk==3.8.1

# Document Processing
PyMuPDF==1.23.8
python-docx==1.1.0
pypdf2==3.0.1
python-pptx==0.6.23
openpyxl==3.1.2

# OCR
pytesseract==0.3.10
opencv-python==4.8.1.78
pillow==10.1.0
google-cloud-vision==3.4.5

# Validation & Serialization
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0.post1

# Authentication & Security
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.2
cryptography==41.0.7

# HTTP Client
httpx==0.25.2
aiofiles==23.2.1
requests==2.31.0

# Monitoring & Metrics
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0
grafana-api==1.0.3

# Logging & Error Tracking
structlog==23.2.0
sentry-sdk==1.38.0

# Development Tools
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1

# API Documentation
openapi-spec-validator==0.7.1

# Data Processing
python-dateutil==2.8.2
pytz==2023.3
faker==20.1.0

# File Format Support
beautifulsoup4==4.12.2
lxml==4.9.3
markdown==3.5.1
python-magic==0.4.27

# Configuration
python-dotenv==1.0.0
click==8.1.7

# Job Matching & Similarity
faiss-cpu==1.7.4
sentence-transformers==2.2.2

# Async Support
asyncio-mqtt==0.16.1
aioredis==2.0.1
aiobotocore==2.7.0
'''

with open("resume_parser_2025/backend/requirements.txt", "w") as f:
    f.write(requirements_content)

print("✅ Requirements file created!")

# Create data models
models_resume_content = '''"""
Resume data models
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Resume(Base):
    """Resume model"""
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False)
    
    # Processing status
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    processing_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Extracted content
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # GDPR compliance
    consent_given = Column(Boolean, default=False)
    consent_timestamp = Column(DateTime, nullable=True)
    anonymized = Column(Boolean, default=False)
    retention_expires_at = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=True)
    candidate = relationship("Candidate", back_populates="resumes")
    
    def __repr__(self):
        return f"<Resume(id={self.id}, filename={self.filename}, status={self.status})>"

class ExtractedEntity(Base):
    """Extracted entities from resume"""
    __tablename__ = "extracted_entities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    
    # Entity information
    entity_type = Column(String(50), nullable=False)  # NAME, EMAIL, PHONE, SKILL, etc.
    entity_value = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    start_position = Column(Integer, nullable=True)
    end_position = Column(Integer, nullable=True)
    
    # Normalized values
    normalized_value = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume")
    
    def __repr__(self):
        return f"<ExtractedEntity(type={self.entity_type}, value={self.entity_value[:50]}...)>"

class Skill(Base):
    """Skills taxonomy"""
    __tablename__ = "skills"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100), nullable=True)
    
    # Skill metadata
    skill_type = Column(String(50), nullable=False)  # technical, soft, language, certification
    proficiency_levels = Column(JSON, nullable=True)  # beginner, intermediate, advanced, expert
    synonyms = Column(JSON, nullable=True)
    related_skills = Column(JSON, nullable=True)
    
    # Industry mapping
    industries = Column(JSON, nullable=True)
    job_roles = Column(JSON, nullable=True)
    
    # Taxonomy IDs
    onet_id = Column(String(50), nullable=True)
    esco_id = Column(String(50), nullable=True)
    
    # Metadata
    popularity_score = Column(Float, default=0.0)
    demand_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Skill(name={self.name}, category={self.category})>"

class ResumeSkill(Base):
    """Resume-Skill relationship with proficiency"""
    __tablename__ = "resume_skills"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    
    # Extracted information
    proficiency_level = Column(String(50), nullable=True)
    years_experience = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=False)
    context = Column(Text, nullable=True)  # Where skill was mentioned
    
    # Verification
    verified = Column(Boolean, default=False)
    verification_source = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume")
    skill = relationship("Skill")
    
    def __repr__(self):
        return f"<ResumeSkill(resume_id={self.resume_id}, skill_id={self.skill_id})>"

class ParsingJob(Base):
    """Async parsing job tracking"""
    __tablename__ = "parsing_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    
    # Job information
    celery_task_id = Column(String(255), nullable=False)
    status = Column(String(20), default="queued")  # queued, running, completed, failed
    priority = Column(Integer, default=5)  # 1-10, lower is higher priority
    
    # Processing details
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    processing_time = Column(Float, nullable=True)
    worker_id = Column(String(255), nullable=True)
    
    # Results
    result = Column(JSON, nullable=True)
    error_details = Column(JSON, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume")
    
    def __repr__(self):
        return f"<ParsingJob(id={self.id}, status={self.status}, task_id={self.celery_task_id})>"
'''

with open("resume_parser_2025/backend/app/models/resume.py", "w") as f:
    f.write(models_resume_content)

print("✅ Resume models created!")

# Create candidate models
models_candidate_content = '''"""
Candidate data models
"""
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .resume import Base

class Candidate(Base):
    """Candidate profile model"""
    __tablename__ = "candidates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Personal Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    
    # Contact Information
    address = Column(JSON, nullable=True)  # street, city, state, country, postal_code
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    portfolio_url = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)
    
    # Professional Information
    current_title = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    total_experience_years = Column(Float, nullable=True)
    current_salary = Column(Integer, nullable=True)
    expected_salary = Column(Integer, nullable=True)
    
    # Availability
    availability = Column(String(50), nullable=True)  # immediate, 2weeks, 1month, etc.
    willing_to_relocate = Column(Boolean, nullable=True)
    work_authorization = Column(String(100), nullable=True)
    
    # Summary
    professional_summary = Column(Text, nullable=True)
    career_objective = Column(Text, nullable=True)
    
    # Metadata
    source = Column(String(100), nullable=True)  # upload, api, scraping, etc.
    tags = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Scoring
    overall_score = Column(Float, nullable=True)
    quality_score = Column(Float, nullable=True)
    completeness_score = Column(Float, nullable=True)
    
    # GDPR Compliance
    consent_marketing = Column(Boolean, default=False)
    consent_data_processing = Column(Boolean, default=False)
    data_retention_until = Column(DateTime, nullable=True)
    anonymized = Column(Boolean, default=False)
    
    # Status
    status = Column(String(50), default="active")  # active, inactive, blacklisted
    verification_status = Column(String(50), default="unverified")
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = Column(DateTime, nullable=True)
    
    # Relationships
    resumes = relationship("Resume", back_populates="candidate")
    work_experiences = relationship("WorkExperience", back_populates="candidate")
    educations = relationship("Education", back_populates="candidate")
    certifications = relationship("Certification", back_populates="candidate")
    languages = relationship("CandidateLanguage", back_populates="candidate")
    projects = relationship("Project", back_populates="candidate")
    
    def __repr__(self):
        return f"<Candidate(id={self.id}, name={self.full_name}, email={self.email})>"

class WorkExperience(Base):
    """Work experience model"""
    __tablename__ = "work_experiences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Job Details
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    company_industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    
    # Location
    location = Column(JSON, nullable=True)  # city, state, country
    
    # Duration
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)
    duration_months = Column(Integer, nullable=True)
    
    # Details
    description = Column(Text, nullable=True)
    achievements = Column(JSON, nullable=True)  # List of achievements
    responsibilities = Column(JSON, nullable=True)  # List of responsibilities
    technologies_used = Column(JSON, nullable=True)  # List of technologies
    
    # Classification
    job_level = Column(String(50), nullable=True)  # entry, mid, senior, lead, executive
    employment_type = Column(String(50), nullable=True)  # full-time, part-time, contract, etc.
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="work_experiences")
    
    def __repr__(self):
        return f"<WorkExperience(title={self.job_title}, company={self.company_name})>"

class Education(Base):
    """Education model"""
    __tablename__ = "educations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Institution
    institution_name = Column(String(255), nullable=False)
    institution_type = Column(String(50), nullable=True)  # university, college, school
    location = Column(JSON, nullable=True)
    
    # Degree Information
    degree_type = Column(String(100), nullable=True)  # Bachelor, Master, PhD, etc.
    field_of_study = Column(String(255), nullable=True)
    major = Column(String(255), nullable=True)
    minor = Column(String(255), nullable=True)
    
    # Academic Performance
    gpa = Column(Float, nullable=True)
    gpa_scale = Column(String(10), nullable=True)  # 4.0, 10.0, etc.
    honors = Column(JSON, nullable=True)  # Dean's list, Magna cum laude, etc.
    
    # Duration
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    graduation_date = Column(DateTime, nullable=True)
    is_ongoing = Column(Boolean, default=False)
    
    # Additional Info
    relevant_coursework = Column(JSON, nullable=True)
    thesis_title = Column(String(500), nullable=True)
    activities = Column(JSON, nullable=True)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="educations")
    
    def __repr__(self):
        return f"<Education(degree={self.degree_type}, field={self.field_of_study}, school={self.institution_name})>"

class Certification(Base):
    """Certification model"""
    __tablename__ = "certifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Certification Details
    name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=False)
    credential_id = Column(String(100), nullable=True)
    credential_url = Column(String(500), nullable=True)
    
    # Dates
    issue_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    does_not_expire = Column(Boolean, default=False)
    
    # Verification
    verification_status = Column(String(50), default="unverified")
    verified_at = Column(DateTime, nullable=True)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="certifications")
    
    def __repr__(self):
        return f"<Certification(name={self.name}, issuer={self.issuing_organization})>"

class CandidateLanguage(Base):
    """Candidate language proficiency"""
    __tablename__ = "candidate_languages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Language Info
    language = Column(String(100), nullable=False)
    proficiency_level = Column(String(50), nullable=True)  # native, fluent, conversational, basic
    
    # Skills breakdown
    speaking_level = Column(String(50), nullable=True)
    writing_level = Column(String(50), nullable=True)
    reading_level = Column(String(50), nullable=True)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="languages")
    
    def __repr__(self):
        return f"<CandidateLanguage(language={self.language}, level={self.proficiency_level})>"

class Project(Base):
    """Candidate projects"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Project Info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    role = Column(String(100), nullable=True)
    
    # Duration
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_ongoing = Column(Boolean, default=False)
    
    # Links
    project_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    
    # Technical Details
    technologies_used = Column(JSON, nullable=True)
    key_achievements = Column(JSON, nullable=True)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="projects")
    
    def __repr__(self):
        return f"<Project(title={self.title}, candidate_id={self.candidate_id})>"
'''

with open("resume_parser_2025/backend/app/models/candidate.py", "w") as f:
    f.write(models_candidate_content)

print("✅ Candidate models created!")

# Create job models
models_job_content = '''"""
Job and matching models
"""
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .resume import Base

class Job(Base):
    """Job posting model"""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Information
    title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    
    # Job Details
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    
    # Classification
    job_type = Column(String(50), nullable=True)  # full-time, part-time, contract, etc.
    job_level = Column(String(50), nullable=True)  # entry, mid, senior, executive
    industry = Column(String(100), nullable=True)
    function = Column(String(100), nullable=True)  # Engineering, Marketing, Sales, etc.
    
    # Location
    location = Column(JSON, nullable=True)  # city, state, country, remote
    is_remote = Column(Boolean, default=False)
    hybrid_policy = Column(String(100), nullable=True)
    
    # Compensation
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), default="USD")
    equity_offered = Column(Boolean, default=False)
    
    # Requirements
    required_skills = Column(JSON, nullable=True)  # List of required skills
    preferred_skills = Column(JSON, nullable=True)  # List of preferred skills
    required_experience_years = Column(Integer, nullable=True)
    required_education = Column(String(100), nullable=True)
    required_certifications = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(50), default="active")  # active, paused, closed, draft
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    # Dates
    posted_date = Column(DateTime, default=datetime.utcnow)
    application_deadline = Column(DateTime, nullable=True)
    expected_start_date = Column(DateTime, nullable=True)
    
    # Metadata
    source = Column(String(100), nullable=True)  # manual, api, scraping
    external_id = Column(String(255), nullable=True)
    external_url = Column(String(500), nullable=True)
    
    # AI Processing
    processed = Column(Boolean, default=False)
    skill_embeddings = Column(JSON, nullable=True)  # Vector embeddings for skills
    description_embeddings = Column(JSON, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=True)
    
    # Relationships
    job_matches = relationship("JobMatch", back_populates="job")
    
    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, company={self.company_name})>"

class JobMatch(Base):
    """Job-Candidate matching results"""
    __tablename__ = "job_matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=True)
    
    # Overall Matching Score
    overall_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Detailed Scores
    skills_score = Column(Float, nullable=True)
    experience_score = Column(Float, nullable=True)
    education_score = Column(Float, nullable=True)
    location_score = Column(Float, nullable=True)
    salary_score = Column(Float, nullable=True)
    
    # Matching Details
    matched_skills = Column(JSON, nullable=True)  # Skills that matched
    missing_skills = Column(JSON, nullable=True)  # Required skills not found
    additional_skills = Column(JSON, nullable=True)  # Extra skills candidate has
    
    # Experience Analysis
    experience_gap = Column(Float, nullable=True)  # Years difference from requirement
    relevant_experience = Column(Float, nullable=True)  # Years of relevant experience
    
    # Education Analysis
    education_level_match = Column(String(50), nullable=True)  # exceeded, met, below
    field_relevance = Column(Float, nullable=True)
    
    # Flags
    is_qualified = Column(Boolean, nullable=True)
    is_overqualified = Column(Boolean, nullable=True)
    is_underqualified = Column(Boolean, nullable=True)
    
    # Recommendations
    recommendation = Column(String(50), nullable=True)  # strong_match, good_match, weak_match, no_match
    reasoning = Column(Text, nullable=True)
    improvement_suggestions = Column(JSON, nullable=True)
    
    # Processing Info
    algorithm_version = Column(String(20), default="v1.0")
    processing_time = Column(Float, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="job_matches")
    candidate = relationship("Candidate")
    resume = relationship("Resume")
    
    def __repr__(self):
        return f"<JobMatch(job_id={self.job_id}, candidate_id={self.candidate_id}, score={self.overall_score})>"

class SkillDemand(Base):
    """Market demand for skills"""
    __tablename__ = "skill_demands"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String(255), nullable=False)
    
    # Demand Metrics
    job_postings_count = Column(Integer, default=0)
    demand_trend = Column(String(20), nullable=True)  # increasing, stable, decreasing
    avg_salary = Column(Float, nullable=True)
    salary_range_min = Column(Float, nullable=True)
    salary_range_max = Column(Float, nullable=True)
    
    # Market Analysis
    industries = Column(JSON, nullable=True)  # Industries where skill is in demand
    job_levels = Column(JSON, nullable=True)  # Job levels requiring this skill
    related_skills = Column(JSON, nullable=True)  # Commonly paired skills
    
    # Temporal Data
    analysis_date = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SkillDemand(skill={self.skill_name}, demand={self.demand_trend})>"

class CandidateJobApplication(Base):
    """Track candidate applications to jobs"""
    __tablename__ = "candidate_job_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=True)
    
    # Application Details
    application_source = Column(String(100), nullable=True)  # website, referral, recruiter
    cover_letter = Column(Text, nullable=True)
    
    # Status Tracking
    status = Column(String(50), default="applied")  # applied, screening, interview, offer, hired, rejected
    stage = Column(String(100), nullable=True)  # phone_screen, technical_interview, final_round
    
    # Feedback
    recruiter_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    interview_feedback = Column(JSON, nullable=True)
    
    # Important Dates
    applied_at = Column(DateTime, default=datetime.utcnow)
    first_contact = Column(DateTime, nullable=True)
    interview_scheduled = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    
    # Outcome
    offered = Column(Boolean, default=False)
    offer_amount = Column(Integer, nullable=True)
    accepted = Column(Boolean, nullable=True)
    hired = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate")
    job = relationship("Job")
    resume = relationship("Resume")
    
    def __repr__(self):
        return f"<Application(candidate_id={self.candidate_id}, job_id={self.job_id}, status={self.status})>"
'''

with open("resume_parser_2025/backend/app/models/job.py", "w") as f:
    f.write(models_job_content)

print("✅ Job models created!")

print("\n🎯 Core data models completed! Created:")
print("- Configuration management")
print("- FastAPI application structure")  
print("- Comprehensive data models for resumes, candidates, jobs")
print("- Requirements file with all dependencies")