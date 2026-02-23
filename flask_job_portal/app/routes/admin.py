"""
Admin Routes
Site administration, user management, analytics
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, User, Job, Application

# Create blueprint
admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """
    Decorator to check if user is admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Admin dashboard with site statistics
    """
    # Get statistics
    total_users = User.query.count()
    total_job_seekers = User.query.filter_by(role='job_seeker').count()
    total_recruiters = User.query.filter_by(role='recruiter').count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Get recent jobs
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_job_seekers=total_job_seekers,
                         total_recruiters=total_recruiters,
                         total_jobs=total_jobs,
                         active_jobs=active_jobs,
                         total_applications=total_applications,
                         recent_users=recent_users,
                         recent_jobs=recent_jobs)


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """
    Manage all users
    """
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/manage_users.html', users=users)


@admin_bp.route('/user/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_user(user_id):
    """
    Deactivate user account
    """
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Cannot deactivate your own account', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user.is_active = False
    db.session.commit()
    flash(f'User {user.username} deactivated', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/user/<int:user_id>/activate', methods=['POST'])
@login_required
@admin_required
def activate_user(user_id):
    """
    Activate user account
    """
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    flash(f'User {user.username} activated', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/jobs')
@login_required
@admin_required
def manage_jobs():
    """
    Manage all job listings
    """
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.paginate(page=page, per_page=20)
    return render_template('admin/manage_jobs.html', jobs=jobs)


@admin_bp.route('/job/<int:job_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_job(job_id):
    """
    Deactivate job listing
    """
    job = Job.query.get_or_404(job_id)
    job.is_active = False
    db.session.commit()
    flash(f'Job "{job.title}" deactivated', 'success')
    return redirect(url_for('admin.manage_jobs'))


@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """
    View site analytics
    """
    # Calculate metrics
    total_applications = Application.query.count()
    avg_match_score = db.session.query(db.func.avg(Application.match_score)).scalar() or 0
    
    # Get applications by status
    status_breakdown = {}
    for status in ['pending', 'reviewed', 'shortlisted', 'rejected', 'accepted']:
        count = Application.query.filter_by(status=status).count()
        status_breakdown[status] = count
    
    # Get top jobs by applications
    top_jobs = db.session.query(
        Job.title, 
        db.func.count(Application.id).label('app_count')
    ).join(Application).group_by(Job.id).order_by(
        db.func.count(Application.id).desc()
    ).limit(10).all()
    
    return render_template('admin/analytics.html',
                         total_applications=total_applications,
                         avg_match_score=round(avg_match_score, 2),
                         status_breakdown=status_breakdown,
                         top_jobs=top_jobs)
