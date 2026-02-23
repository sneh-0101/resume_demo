"""
Database Models Package
Contains all SQLAlchemy ORM models for the Job Portal
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy - will be configured in app factory
db = SQLAlchemy()


class User(db.Model):
    """
    User Model - Represents registered users
    Roles: job_seeker, recruiter, admin
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='job_seeker')  # job_seeker, recruiter, admin
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)  # For job seekers - professional bio
    company = db.Column(db.String(255))  # For recruiters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')
    jobs = db.relationship('Job', backref='recruiter', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'


class Job(db.Model):
    """
    Job Model - Represents job postings created by recruiters
    """
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)  # Required skills/qualifications
    location = db.Column(db.String(255))
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    job_type = db.Column(db.String(50), default='Full-time')  # Full-time, Part-time, Remote, etc.
    company = db.Column(db.String(255))
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def get_application_count(self):
        """Get total applications for this job"""
        return len(self.applications)
    
    def __repr__(self):
        return f'<Job {self.title}>'


class Resume(db.Model):
    """
    Resume Model - Stores uploaded resumes for job seekers
    """
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text)  # Text extracted from PDF
    extracted_skills = db.Column(db.JSON)  # Skills extracted from resume
    is_primary = db.Column(db.Boolean, default=False)  # Primary resume for matching
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resume {self.filename}>'


class Application(db.Model):
    """
    Application Model - Tracks job applications by job seekers
    """
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    status = db.Column(db.String(50), default='pending')  # pending, reviewed, shortlisted, rejected, accepted
    match_score = db.Column(db.Float)  # AI-calculated match score (0-100)
    matched_skills = db.Column(db.JSON)  # Skills that matched
    missing_skills = db.Column(db.JSON)  # Skills that didn't match
    cover_letter = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resume = db.relationship('Resume', backref='applications')
    
    def __repr__(self):
        return f'<Application {self.id}>'
