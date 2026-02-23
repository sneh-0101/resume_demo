"""
Recruiter Routes
Job posting, application management, dashboard
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, Job, Application, User

# Create blueprint
recruiter_bp = Blueprint('recruiter', __name__)


def recruiter_required(f):
    """
    Decorator to check if user is recruiter
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'recruiter':
            flash('Access denied. Recruiter access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@recruiter_bp.route('/dashboard')
@login_required
@recruiter_required
def dashboard():
    """
    Recruiter dashboard
    Shows job postings and application statistics
    """
    # Get recruiter's jobs
    jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
    
    # Calculate statistics
    total_jobs = len(jobs)
    total_applications = sum(len(job.applications) for job in jobs)
    pending_applications = Application.query.join(Job).filter(
        Job.recruiter_id == current_user.id,
        Application.status == 'pending'
    ).count()
    
    # Get recent applications
    recent_apps = Application.query.join(Job).filter(
        Job.recruiter_id == current_user.id
    ).order_by(Application.applied_at.desc()).limit(10).all()
    
    return render_template('recruiter/dashboard.html',
                         jobs=jobs,
                         total_jobs=total_jobs,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         recent_apps=recent_apps)


@recruiter_bp.route('/job/create', methods=['GET', 'POST'])
@login_required
@recruiter_required
def create_job():
    """
    Create new job posting
    """
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        job_type = request.form.get('job_type', 'Full-time')
        salary_min = request.form.get('salary_min', type=float)
        salary_max = request.form.get('salary_max', type=float)
        
        # Validation
        if not all([title, description, requirements]):
            flash('Title, description, and requirements are required', 'danger')
            return redirect(url_for('recruiter.create_job'))
        
        # Create job
        job = Job(
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            job_type=job_type,
            salary_min=salary_min,
            salary_max=salary_max,
            company=current_user.company,
            recruiter_id=current_user.id
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash(f'Job "{title}" posted successfully!', 'success')
        return redirect(url_for('recruiter.dashboard'))
    
    return render_template('recruiter/create_job.html')


@recruiter_bp.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
@recruiter_required
def edit_job(job_id):
    """
    Edit job posting
    """
    job = Job.query.get_or_404(job_id)
    
    # Check ownership
    if job.recruiter_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('recruiter.dashboard'))
    
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.requirements = request.form.get('requirements')
        job.location = request.form.get('location')
        job.job_type = request.form.get('job_type')
        job.salary_min = request.form.get('salary_min', type=float)
        job.salary_max = request.form.get('salary_max', type=float)
        
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('recruiter.dashboard'))
    
    return render_template('recruiter/edit_job.html', job=job)


@recruiter_bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
@recruiter_required
def delete_job(job_id):
    """
    Delete job posting
    """
    job = Job.query.get_or_404(job_id)
    
    # Check ownership
    if job.recruiter_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('recruiter.dashboard'))
    
    # Delete job and related applications
    db.session.delete(job)
    db.session.commit()
    
    flash('Job deleted successfully', 'success')
    return redirect(url_for('recruiter.dashboard'))


@recruiter_bp.route('/applications')
@login_required
@recruiter_required
def manage_applications():
    """
    Manage applications for recruiter's jobs
    """
    # Get applications for recruiter's jobs
    applications = Application.query.join(Job).filter(
        Job.recruiter_id == current_user.id
    ).order_by(Application.applied_at.desc()).all()
    
    # Group by status
    by_status = {
        'pending': [a for a in applications if a.status == 'pending'],
        'reviewed': [a for a in applications if a.status == 'reviewed'],
        'shortlisted': [a for a in applications if a.status == 'shortlisted'],
        'rejected': [a for a in applications if a.status == 'rejected']
    }
    
    return render_template('recruiter/manage_applications.html', 
                         applications=applications,
                         by_status=by_status)


@recruiter_bp.route('/application/<int:app_id>/update', methods=['POST'])
@login_required
@recruiter_required
def update_application_status(app_id):
    """
    Update application status
    """
    app = Application.query.get_or_404(app_id)
    job = app.job
    
    # Check ownership
    if job.recruiter_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('recruiter.manage_applications'))
    
    new_status = request.form.get('status')
    if new_status in ['pending', 'reviewed', 'shortlisted', 'rejected', 'accepted']:
        app.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}', 'success')
    
    return redirect(url_for('recruiter.manage_applications'))
