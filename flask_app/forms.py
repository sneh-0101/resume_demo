"""
WTForms for form validation and rendering
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, Optional
from flask_app.models import User


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        Regexp('^[A-Za-z0-9_]+$', message='Username must contain only letters, numbers, and underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    first_name = StringField('First Name', validators=[
        Length(max=100, message='First name must be less than 100 characters')
    ])
    last_name = StringField('Last Name', validators=[
        Length(max=100, message='Last name must be less than 100 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(message='Password confirmation is required'),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Register As', choices=[
        ('user', 'User (Job Seeker)'),
        ('hr', 'HR (Recruiter)'),
        ('admin', 'Admin')
    ], default='user', validators=[DataRequired()])
    admin_code = StringField('Admin Secret Code', validators=[Optional()])
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    submit = SubmitField('Login')


class ResumeUploadForm(FlaskForm):
    """Resume upload form"""
    resume_file = FileField('Upload Resume (PDF)', validators=[
        DataRequired(message='Please select a resume file'),
        FileAllowed(['pdf'], message='Only PDF files are allowed')
    ])
    submit = SubmitField('Upload Resume')


class JobMatchingForm(FlaskForm):
    """Job matching form"""
    job_description = TextAreaField('Job Description', validators=[
        DataRequired(message='Job description is required'),
        Length(min=50, max=5000, message='Job description must be between 50 and 5000 characters')
    ])
    submit = SubmitField('Analyze Match')


class QuickAnalysisForm(FlaskForm):
    """Quick analysis form for ad-hoc uploads"""
    resume_file = FileField('Upload Resume (PDF)', validators=[
        DataRequired(message='Please select a resume file'),
        FileAllowed(['pdf'], message='Only PDF files are allowed')
    ])
    job_description = TextAreaField('Job Description', validators=[
        DataRequired(message='Job description is required'),
        Length(min=50, max=5000, message='Job description must be between 50 and 5000 characters')
    ])
    submit = SubmitField('Analyze')

class JobPostingForm(FlaskForm):
    """Job posting form for HR users"""
    title = StringField('Job Title', validators=[
        DataRequired(message='Job title is required'),
        Length(max=255, message='Title must be less than 255 characters')
    ])
    company = StringField('Company Name', validators=[
        DataRequired(message='Company name is required'),
        Length(max=255, message='Company name must be less than 255 characters')
    ])
    description = TextAreaField('Job Description', validators=[
        DataRequired(message='Job description is required'),
        Length(min=50, max=5000, message='Description must be between 50 and 5000 characters')
    ])
    required_skills = StringField('Required Skills (comma-separated)', validators=[
        Optional(),
        Length(max=500, message='Skills must be less than 500 characters')
    ])
    salary_min = StringField('Minimum Salary', validators=[Optional()])
    salary_max = StringField('Maximum Salary', validators=[Optional()])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=255, message='Location must be less than 255 characters')
    ])
    job_url = StringField('Job URL', validators=[
        Optional(),
        Length(max=500, message='URL must be less than 500 characters')
    ])
    submit = SubmitField('Post Job')


class EducationEntryForm(Form):
    """Education entry sub-form"""
    school = StringField('School', validators=[DataRequired(message='School is required'), Length(max=255)])
    degree = StringField('Degree', validators=[Optional(), Length(max=255)])
    field_of_study = StringField('Field of Study', validators=[Optional(), Length(max=255)])
    
    start_month = SelectField('Start Month', choices=[('', 'Month')] + [(str(i), str(i)) for i in range(1, 13)], validators=[Optional()])
    start_year = StringField('Start Year', validators=[Optional(), Length(max=4)])
    
    end_month = SelectField('End Month', choices=[('', 'Month')] + [(str(i), str(i)) for i in range(1, 13)], validators=[Optional()])
    end_year = StringField('End Year', validators=[Optional(), Length(max=4)])
    
    grade = StringField('Grade', validators=[Optional(), Length(max=80)])
    activities = TextAreaField('Activities and societies', validators=[Optional(), Length(max=500)])
    details = TextAreaField('Description', validators=[Optional()])

class ExperienceEntryForm(Form):
    """Experience entry sub-form"""
    role = StringField('Role / Position', validators=[DataRequired(message='Role is required'), Length(max=255)])
    company = StringField('Company', validators=[DataRequired(message='Company is required'), Length(max=255)])
    location = StringField('Location', validators=[Optional(), Length(max=255)])
    
    start_month = SelectField('Start Month', choices=[('', 'Month')] + [(str(i), str(i)) for i in range(1, 13)], validators=[Optional()])
    start_year = StringField('Start Year', validators=[Optional(), Length(max=4)])
    
    end_month = SelectField('End Month', choices=[('', 'Month')] + [(str(i), str(i)) for i in range(1, 13)], validators=[Optional()])
    end_year = StringField('End Year', validators=[Optional(), Length(max=4)])
    
    details = TextAreaField('Description', validators=[Optional()])

class ResumeBuilderForm(FlaskForm):
    """Resume builder details form (Redesigned)"""
    # Personal Info
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    linkedin = StringField('LinkedIn URL', validators=[Optional(), Length(max=255)])
    github = StringField('GitHub URL', validators=[Optional(), Length(max=255)])
    
    # Career Content
    career_objective = TextAreaField('Career Objective', validators=[Optional()])
    
    # Skills, Certifications, Achievements (comma-separated)
    skills = StringField('Skills (comma-separated)', validators=[Optional()])
    certifications = StringField('Certifications (comma-separated)', validators=[Optional()])
    achievements = StringField('Achievements (comma-separated)', validators=[Optional()])
    
    # Structured lists (will be handled by JavaScript cloning on the frontend)
    # We use FieldList to allow multiple entries, but for the initial render we'll handle the dynamic part in templates
    education_list = FieldList(FormField(EducationEntryForm), min_entries=0)
    experience_list = FieldList(FormField(ExperienceEntryForm), min_entries=0)
    
    # For projects we'll keep it simple or also add FieldList
    projects = TextAreaField('Projects (Format: Title \n Link \n Description - separated by double newlines)', validators=[Optional()])
    
    submit = SubmitField('Generate Resume')
