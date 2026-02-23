"""
Job Seeker Routes
Resume upload, job applications, AI-based matching, dashboard
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
import os
from app.models import db, Resume, Job, Application, User
from app.ai_engine import ResumeParser, SkillMatcher

# Create blueprint
job_seeker_bp = Blueprint('job_seeker', __name__)


def job_seeker_required(f):
    """
    Decorator to check if user is job seeker
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'job_seeker':
            flash('Access denied. Job Seeker access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed"""
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@job_seeker_bp.route('/dashboard')
@login_required
@job_seeker_required
def dashboard():
    """
    Job seeker dashboard
    Shows applications, matched jobs, and resume status
    """
    # Get user's applications
    applications = Application.query.filter_by(user_id=current_user.id).order_by(
        Application.applied_at.desc()
    ).all()
    
    # Get user's resumes
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    
    # Calculate statistics
    total_applications = len(applications)
    shortlisted = sum(1 for a in applications if a.status == 'shortlisted')
    rejected = sum(1 for a in applications if a.status == 'rejected')
    accepted = sum(1 for a in applications if a.status == 'accepted')
    
    return render_template('job_seeker/dashboard.html',
                         applications=applications,
                         resumes=resumes,
                         total_applications=total_applications,
                         shortlisted=shortlisted,
                         rejected=rejected,
                         accepted=accepted)


@job_seeker_bp.route('/resume/upload', methods=['GET', 'POST'])
@login_required
@job_seeker_required
def upload_resume():
    """
    Upload resume file
    """
    from flask import current_app
    
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('job_seeker.upload_resume'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('job_seeker.upload_resume'))
        
        if not allowed_file(file.filename):
            flash('Only PDF files are allowed', 'danger')
            return redirect(url_for('job_seeker.upload_resume'))
        
        try:
            # Save file
            filename = secure_filename(file.filename)
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
            os.makedirs(user_folder, exist_ok=True)
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)
            
            # Extract resume text
            parser = ResumeParser()
            resume_text = parser.extract_text(filepath)
            
            # Extract skills
            skills = list(SkillMatcher.extract_skills(resume_text))
            
            # Create resume record
            resume = Resume(
                user_id=current_user.id,
                filename=filename,
                filepath=filepath,
                extracted_text=resume_text,
                extracted_skills=skills
            )
            
            db.session.add(resume)
            db.session.commit()
            
            flash(f'Resume "{filename}" uploaded successfully!', 'success')
            return redirect(url_for('job_seeker.dashboard'))
        
        except Exception as e:
            flash(f'Error uploading resume: {str(e)}', 'danger')
            return redirect(url_for('job_seeker.upload_resume'))
    
    return render_template('job_seeker/upload_resume.html')


@job_seeker_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
@job_seeker_required
def apply_job(job_id):
    """
    Apply for a job with resume and optional cover letter
    Includes AI-based resume matching
    """
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing_app = Application.query.filter_by(
        user_id=current_user.id,
        job_id=job_id
    ).first()
    
    if existing_app:
        flash('You have already applied for this job', 'info')
        return redirect(url_for('main.view_job', job_id=job_id))
    
    if request.method == 'POST':
        resume_id = request.form.get('resume_id', type=int)
        cover_letter = request.form.get('cover_letter', '')
        
        if not resume_id:
            flash('Please select a resume', 'danger')
            return redirect(url_for('job_seeker.apply_job', job_id=job_id))
        
        # Get resume
        resume = Resume.query.get_or_404(resume_id)
        
        if resume.user_id != current_user.id:
            flash('Access denied', 'danger')
            return redirect(url_for('main.view_job', job_id=job_id))
        
        try:
            # AI-based matching
            matcher = SkillMatcher()
            match_result = matcher.analyze_match(
                resume.extracted_text,
                job.description,
                job.requirements
            )
            
            # Create application
            application = Application(
                job_id=job_id,
                user_id=current_user.id,
                resume_id=resume_id,
                cover_letter=cover_letter,
                match_score=match_result['overall_score'],
                matched_skills=match_result['matched_skills'],
                missing_skills=match_result['missing_skills'],
                status='pending'
            )
            
            db.session.add(application)
            db.session.commit()
            
            flash(f'Application submitted! Match score: {match_result["overall_score"]}%', 'success')
            return redirect(url_for('job_seeker.view_application', app_id=application.id))
        
        except Exception as e:
            flash(f'Error submitting application: {str(e)}', 'danger')
            return redirect(url_for('job_seeker.apply_job', job_id=job_id))
    
    # Get user's resumes
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    
    return render_template('job_seeker/apply.html', job=job, resumes=resumes)


@job_seeker_bp.route('/application/<int:app_id>')
@login_required
@job_seeker_required
def view_application(app_id):
    """
    View application details with match results
    """
    application = Application.query.get_or_404(app_id)
    
    # Check ownership
    if application.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('job_seeker.dashboard'))
    
    return render_template('job_seeker/application_detail.html', application=application)


@job_seeker_bp.route('/applications')
@login_required
@job_seeker_required
def my_applications():
    """
    View all applications
    """
    applications = Application.query.filter_by(user_id=current_user.id).order_by(
        Application.applied_at.desc()
    ).all()
    
    return render_template('job_seeker/my_applications.html', applications=applications)


@job_seeker_bp.route('/resume/<int:resume_id>/delete', methods=['POST'])
@login_required
@job_seeker_required
def delete_resume(resume_id):
    """
    Delete resume file
    """
    resume = Resume.query.get_or_404(resume_id)
    
    # Check ownership
    if resume.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('job_seeker.dashboard'))
    
    # Delete file
    if os.path.exists(resume.filepath):
        os.remove(resume.filepath)
    
    # Delete record
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully', 'success')
    return redirect(url_for('job_seeker.dashboard'))


@job_seeker_bp.route('/resume/<int:resume_id>/download')
@login_required
@job_seeker_required
def download_resume(resume_id):
    """
    Download resume file
    """
    resume = Resume.query.get_or_404(resume_id)
    
    # Check ownership
    if resume.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('job_seeker.dashboard'))
    
    return send_file(resume.filepath, as_attachment=True)
