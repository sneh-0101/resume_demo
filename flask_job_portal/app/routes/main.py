"""
Main Routes (Fixed)
Home page and general routes
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Job, Application, User

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Home page
    Shows job statistics and featured jobs
    """
    try:
        # Get statistics
        total_jobs = Job.query.filter_by(is_active=True).count()
        total_companies = db.session.query(User.company).filter(
            User.role == 'recruiter'
        ).distinct().count()
        total_applications = Application.query.count()
        
        # Get featured jobs (latest 6)
        featured_jobs = Job.query.filter_by(is_active=True).order_by(
            Job.created_at.desc()
        ).limit(6).all()
        
        return render_template('index.html', 
                             total_jobs=total_jobs,
                             total_companies=total_companies,
                             total_applications=total_applications,
                             featured_jobs=featured_jobs)
    except Exception as e:
        # Fallback if query fails
        return render_template('index.html', 
                             total_jobs=0,
                             total_companies=0,
                             total_applications=0,
                             featured_jobs=[])


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Redirect to role-specific dashboard
    """
    from flask import redirect, url_for
    
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'recruiter':
        return redirect(url_for('recruiter.dashboard'))
    else:
        return redirect(url_for('job_seeker.dashboard'))


@main_bp.route('/jobs')
def browse_jobs():
    """
    Browse all job listings
    """
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('job_type', '')
    
    # Build query
    query = Job.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            (Job.title.ilike(f'%{search}%')) | 
            (Job.description.ilike(f'%{search}%'))
        )
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    
    if job_type:
        query = query.filter(Job.job_type == job_type)
    
    # Paginate
    jobs = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('jobs/browse.html', jobs=jobs, search=search, 
                         location=location, job_type=job_type)


@main_bp.route('/job/<int:job_id>')
def view_job(job_id):
    """
    View detailed job posting
    """
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    has_applied = False
    if current_user.is_authenticated:
        has_applied = Application.query.filter_by(
            user_id=current_user.id,
            job_id=job_id
        ).first() is not None
    
    # Get applications count
    applications_count = Application.query.filter_by(job_id=job_id).count()
    
    return render_template('jobs/detail.html', job=job, has_applied=has_applied,
                         applications_count=applications_count)
