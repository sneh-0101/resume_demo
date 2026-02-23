"""
Database Models
"""

from flask_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Admin fields
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    analyses = db.relationship('Analysis', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Resume(db.Model):
    """Resume model for stored resumes"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text)
    extracted_skills = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resume {self.filename}>'


class JobPosting(db.Model):
    """Job posting model"""
    __tablename__ = 'job_postings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON, default=list)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    location = db.Column(db.String(255))
    job_url = db.Column(db.String(500))
    posted_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<JobPosting {self.title} @ {self.company}>'


class Analysis(db.Model):
    """Analysis results model"""
    __tablename__ = 'analyses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.String(36), db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.String(36), db.ForeignKey('job_postings.id'), nullable=True)
    
    # Analysis data
    match_score = db.Column(db.Float, default=0.0)
    matched_skills = db.Column(db.JSON, default=list)
    missing_skills = db.Column(db.JSON, default=list)
    suggestions = db.Column(db.JSON, default=list)
    match_percentage = db.Column(db.Integer, default=0)
    
    # ATS Friendly data
    ats_score = db.Column(db.Float, default=0.0)
    ats_details = db.Column(db.JSON, default=dict)
    
    # New Features
    interview_questions = db.Column(db.JSON, default=list)
    skill_resources = db.Column(db.JSON, default=list)

    
    # Job description input (if not from job posting)
    job_description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analysis {self.id} - Score: {self.match_score}>'


class ResumeData(db.Model):
    """Model to store resume builder data"""
    __tablename__ = 'resume_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Personal Info
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    
    # Career Content
    career_objective = db.Column(db.Text)
    
    # Complex fields stored as JSON
    education = db.Column(db.JSON, default=list) # [{school, degree, year, gpa}]
    experience = db.Column(db.JSON, default=list) # [{company, role, duration, description}]
    projects = db.Column(db.JSON, default=list) # [{title, link, description}]
    skills = db.Column(db.JSON, default=list) # [skill1, skill2]
    certifications = db.Column(db.JSON, default=list) # [cert1, cert2]
    achievements = db.Column(db.JSON, default=list) # [ach1, ach2]
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResumeData {self.full_name}>'
