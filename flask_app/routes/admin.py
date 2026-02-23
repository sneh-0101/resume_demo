from flask import Blueprint, render_template, redirect, url_for, flash, abort, send_file

from flask_login import login_required, current_user
from functools import wraps
from flask_app.models import User, Resume, Analysis, JobPosting
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Fetch statistics
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    total_analyses = Analysis.query.count()
    total_jobs = JobPosting.query.count()
    
    # User distribution
    users = User.query.all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_resumes=total_resumes,
                         total_analyses=total_analyses,
                         total_jobs=total_jobs,
                         users=users)


@admin_bp.route('/user_resumes/<string:user_id>')
@login_required
@admin_required
def user_resumes(user_id):
    # Get user information
    user = User.query.get_or_404(user_id)
    
    # Get user's resumes
    resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.created_at.desc()).all()
    
    return render_template('admin/user_resumes.html',
                         user=user,
                         resumes=resumes)


@admin_bp.route('/download_resume/<string:resume_id>')
@login_required
@admin_required
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    
    # Construct the correct file path
    import os
    from flask import current_app
    
    # Get the uploads directory from the app config
    uploads_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    user_upload_dir = os.path.join(uploads_dir, resume.user_id)
    
    # Debug information
    print(f"DEBUG: Looking for resume: {resume.filename}")
    print(f"DEBUG: User upload dir: {user_upload_dir}")
    print(f"DEBUG: Directory exists: {os.path.exists(user_upload_dir)}")
    
    # Try to find the file by searching in the user's upload directory
    actual_file_path = None
    
    if os.path.exists(user_upload_dir):
        # Look for files that contain the resume filename (try multiple patterns)
        search_patterns = [
            resume.filename.replace(' ', '_'),  # My Resume (1).pdf -> My_Resume_(1).pdf
            resume.filename.replace(' ', '_').replace('(', '').replace(')', ''),  # My Resume (1).pdf -> My_Resume_1.pdf
            resume.filename.replace(' ', '_').replace('(', '_').replace(')', '_'),  # My Resume (1).pdf -> My_Resume__1_.pdf
            resume.filename.replace('(', '').replace(')', ''),  # My Resume (1).pdf -> My Resume 1.pdf
        ]
        
        print(f"DEBUG: Search patterns: {search_patterns}")
        
        for filename in os.listdir(user_upload_dir):
            print(f"DEBUG: Checking file: {filename}")
            if filename.endswith('.pdf'):
                for pattern in search_patterns:
                    if pattern in filename:
                        actual_file_path = os.path.join(user_upload_dir, filename)
                        print(f"DEBUG: MATCH FOUND! Pattern: {pattern}, File: {filename}")
                        break
                if actual_file_path:
                    break
    
    # If not found, try the original path patterns
    if not actual_file_path:
        print("DEBUG: Trying fallback patterns...")
        possible_paths = [
            resume.filepath,  # Original path from database
            os.path.join(uploads_dir, resume.filename),  # Direct in uploads
            os.path.join(user_upload_dir, resume.filename),  # In user folder
            os.path.join(user_upload_dir, f"{resume.id}_{resume.filename}"),  # With ID prefix
            os.path.join(user_upload_dir, f"{resume.id}_{resume.filename.replace(' ', '_')}"),  # With spaces replaced
        ]
        
        for path in possible_paths:
            print(f"DEBUG: Checking path: {path}")
            if path and os.path.exists(path):
                actual_file_path = path
                print(f"DEBUG: FALLBACK MATCH: {path}")
                break
    
    if not actual_file_path:
        print(f"DEBUG: File not found for: {resume.filename}")
        flash(f'Resume file not found for: {resume.filename}', 'error')
        return redirect(url_for('admin.user_resumes', user_id=resume.user_id))
    
    print(f"DEBUG: Successfully found file: {actual_file_path}")
    return send_file(actual_file_path, as_attachment=True, download_name=resume.filename)
