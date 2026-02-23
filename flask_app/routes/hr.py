"""HR routes for job posting management"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from flask_app import db
from flask_app.models import JobPosting, User, Resume, Analysis
from flask_app.forms import JobPostingForm

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

def hr_required(f):
    """Decorator to require HR role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'hr':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@hr_bp.route('/')
@login_required
@hr_required
def dashboard():
    """HR dashboard"""
    jobs_count = JobPosting.query.filter_by(posted_by=current_user.id).count()
    total_users = User.query.filter_by(role='user').count()
    total_resumes = Resume.query.count()
    
    return render_template('hr/dashboard.html',
                         jobs_count=jobs_count,
                         total_users=total_users,
                         total_resumes=total_resumes)

@hr_bp.route('/jobs')
@login_required
@hr_required
def jobs():
    """List all jobs posted by this HR user"""
    job_listings = JobPosting.query.filter_by(posted_by=current_user.id).order_by(JobPosting.created_at.desc()).all()
    return render_template('hr/jobs.html', jobs=job_listings)

@hr_bp.route('/jobs/add', methods=['GET', 'POST'])
@login_required
@hr_required
def add_job():
    """Add new job posting"""
    form = JobPostingForm()
    if form.validate_on_submit():
        # Parse skills
        skills_list = [s.strip() for s in form.required_skills.data.split(',')] if form.required_skills.data else []
        
        # Parse salary
        try:
            salary_min = float(form.salary_min.data) if form.salary_min.data else None
            salary_max = float(form.salary_max.data) if form.salary_max.data else None
        except ValueError:
            salary_min = None
            salary_max = None
        
        job = JobPosting(
            title=form.title.data,
            company=form.company.data,
            description=form.description.data,
            required_skills=skills_list,
            salary_min=salary_min,
            salary_max=salary_max,
            location=form.location.data,
            job_url=form.job_url.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        
        flash(f'Job "{job.title}" posted successfully!', 'success')
        return redirect(url_for('hr.jobs'))
    
    return render_template('hr/job_form.html', form=form, title='Add New Job')

@hr_bp.route('/jobs/<job_id>/edit', methods=['GET', 'POST'])
@login_required
@hr_required
def edit_job(job_id):
    """Edit existing job posting"""
    job = JobPosting.query.get_or_404(job_id)
    
    # Ensure HR can only edit their own jobs
    if job.posted_by != current_user.id:
        abort(403)
    
    form = JobPostingForm()
    if form.validate_on_submit():
        skills_list = [s.strip() for s in form.required_skills.data.split(',')] if form.required_skills.data else []
        
        try:
            salary_min = float(form.salary_min.data) if form.salary_min.data else None
            salary_max = float(form.salary_max.data) if form.salary_max.data else None
        except ValueError:
            salary_min = None
            salary_max = None
        
        job.title = form.title.data
        job.company = form.company.data
        job.description = form.description.data
        job.required_skills = skills_list
        job.salary_min = salary_min
        job.salary_max = salary_max
        job.location = form.location.data
        job.job_url = form.job_url.data
        
        db.session.commit()
        flash(f'Job "{job.title}" updated successfully!', 'success')
        return redirect(url_for('hr.jobs'))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = job.title
        form.company.data = job.company
        form.description.data = job.description
        form.required_skills.data = ', '.join(job.required_skills) if job.required_skills else ''
        form.salary_min.data = str(job.salary_min) if job.salary_min else ''
        form.salary_max.data = str(job.salary_max) if job.salary_max else ''
        form.location.data = job.location
        form.job_url.data = job.job_url
    
    return render_template('hr/job_form.html', form=form, title='Edit Job', job=job)

@hr_bp.route('/jobs/<job_id>/delete', methods=['POST'])
@login_required
@hr_required
def delete_job(job_id):
    """Delete job posting"""
    job = JobPosting.query.get_or_404(job_id)
    
    if job.posted_by != current_user.id:
        abort(403)
    
    job_title = job.title
    db.session.delete(job)
    db.session.commit()
    
    flash(f'Job "{job_title}" deleted successfully!', 'success')
    return redirect(url_for('hr.jobs'))
