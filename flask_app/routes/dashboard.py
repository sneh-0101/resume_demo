"""
Dashboard routes
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_app.models import Resume, Analysis

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('')
@login_required
def index():
    """Main dashboard"""
    resume_count = Resume.query.filter_by(user_id=current_user.id).count()
    analysis_count = Analysis.query.filter_by(user_id=current_user.id).count()
    
    # Get recent analyses
    recent_analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    
    # Calculate average score
    analyses = Analysis.query.filter_by(user_id=current_user.id).all()
    avg_score = sum(a.match_score for a in analyses) / len(analyses) if analyses else 0
    
    return render_template('dashboard/index.html',
                         resume_count=resume_count,
                         analysis_count=analysis_count,
                         avg_score=round(avg_score, 2),
                         recent_analyses=recent_analyses)


@dashboard_bp.route('profile')
@login_required
def profile():
    """User profile page"""
    return render_template('dashboard/profile.html')
