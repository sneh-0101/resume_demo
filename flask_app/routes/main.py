"""
Main routes for index and general pages
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from sqlalchemy import func
from flask_app import db
from flask_app.models import Resume, Analysis

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard - requires login"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=url_for('main.dashboard')))
        
    # Get stats
    resume_count = Resume.query.filter_by(user_id=current_user.id).count()
    analysis_count = Analysis.query.filter_by(user_id=current_user.id).count()
    
    # Calculate average score
    avg_score_result = db.session.query(func.avg(Analysis.match_score)).filter_by(user_id=current_user.id).scalar()
    avg_score = round(avg_score_result, 1) if avg_score_result else 0
    
    # Get recent analyses
    recent_analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         resume_count=resume_count,
                         analysis_count=analysis_count,
                         avg_score=avg_score,
                         recent_analyses=recent_analyses)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/features')
def features():
    """Features page"""
    return render_template('features.html')
