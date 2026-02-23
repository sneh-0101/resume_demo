"""
Resume Builder routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from flask_app import db
from flask_app.models import ResumeData
from flask_app.forms import ResumeBuilderForm
import json
import io

resume_bp = Blueprint('resume', __name__, url_prefix='/resume-builder')

@resume_bp.app_context_processor
def utility_processor():
    # Deprecated: CSS is now handled via standard link tags in templates
    return dict(include_static_css=lambda x: "")

@resume_bp.route('/', methods=['GET', 'POST'])
@login_required
def builder():
    """Resume builder form"""
    # Check if user already has data
    resume_data = ResumeData.query.filter_by(user_id=current_user.id).first()
    form = ResumeBuilderForm()
    
    if request.method == 'GET' and resume_data:
        # Pre-fill form
        form.full_name.data = resume_data.full_name
        form.email.data = resume_data.email
        form.phone.data = resume_data.phone
        form.linkedin.data = resume_data.linkedin
        form.github.data = resume_data.github
        form.career_objective.data = resume_data.career_objective
        form.skills.data = ", ".join(resume_data.skills) if resume_data.skills else ""
        form.certifications.data = ", ".join(resume_data.certifications) if resume_data.certifications else ""
        form.achievements.data = ", ".join(resume_data.achievements) if resume_data.achievements else ""
        
        # Populate FieldLists
        if resume_data.education:
            for edu in resume_data.education:
                # Map 'description' (DB) to 'details' (Form) to avoid name collision
                edu_copy = edu.copy()
                if 'description' in edu_copy:
                    edu_copy['details'] = edu_copy.pop('description')
                form.education_list.append_entry(edu_copy)
                
        if resume_data.experience:
            for exp in resume_data.experience:
                # Map 'description' (DB) to 'details' (Form) to avoid name collision
                exp_copy = exp.copy()
                if 'description' in exp_copy:
                    exp_copy['details'] = exp_copy.pop('description')
                form.experience_list.append_entry(exp_copy)
                
        if resume_data.projects:
            prj_text = ""
            for prj in resume_data.projects:
                prj_text += f"{prj.get('title')}\n{prj.get('link')}\n{prj.get('description')}\n\n"
            form.projects.data = prj_text.strip()

    if form.validate_on_submit():
        # Process and save data
        if not resume_data:
            resume_data = ResumeData(user_id=current_user.id)
            db.session.add(resume_data)
            
        resume_data.full_name = form.full_name.data
        resume_data.email = form.email.data
        resume_data.phone = form.phone.data
        resume_data.linkedin = form.linkedin.data
        resume_data.github = form.github.data
        resume_data.career_objective = form.career_objective.data
        
        # Convert strings to lists
        resume_data.skills = [s.strip() for s in form.skills.data.split(',') if s.strip()]
        resume_data.certifications = [s.strip() for s in form.certifications.data.split(',') if s.strip()]
        resume_data.achievements = [s.strip() for s in form.achievements.data.split(',') if s.strip()]
        
        # Collect from FieldLists and map 'details' (Form) back to 'description' (DB)
        education_data = []
        for edu_form in form.education_list:
            data = edu_form.data
            if 'details' in data:
                data['description'] = data.pop('details')
            education_data.append(data)
        resume_data.education = education_data
        
        experience_data = []
        for exp_form in form.experience_list:
            data = exp_form.data
            if 'details' in data:
                data['description'] = data.pop('details')
            experience_data.append(data)
        resume_data.experience = experience_data
        
        projects_list = []
        if form.projects.data:
            blocks = form.projects.data.split('\n\n')
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 1:
                    title = lines[0].strip()
                    link = lines[1].strip() if len(lines) > 1 else ""
                    description = "\n".join(lines[2:]) if len(lines) > 2 else ""
                    projects_list.append({'title': title, 'link': link, 'description': description})
        resume_data.projects = projects_list
        
        db.session.commit()
        flash('Resume details saved successfully!', 'success')
        return redirect(url_for('resume.templates'))
        
    return render_template('resume_builder/resume_form.html', form=form)

RESUME_TEMPLATES = [
    {
        'id': 1,
        'name': 'Modern Professional',
        'description': 'Clean, modern layout with distinct sections. Great for tech and business roles.',
        'preview': 'modern_prof.jpg'
    },
    {
        'id': 2,
        'name': 'ATS Ultra Minimal',
        'description': 'Standard black & white design optimized for Applicant Tracking Systems.',
        'preview': 'ats_min.jpg'
    },
    {
        'id': 3,
        'name': 'Left Sidebar Modern',
        'description': 'Elegant sidebar layout providing a balanced and organized visual structure.',
        'preview': 'sidebar_modern.jpg'
    },
    {
        'id': 4,
        'name': 'Executive Corporate',
        'description': 'Sophisticated serif typography suitable for senior and corporate positions.',
        'preview': 'executive.jpg'
    },
    {
        'id': 5,
        'name': 'Creative Clean',
        'description': 'A fresh, imaginative layout for designers and creative professionals.',
        'preview': 'creative.jpg'
    },
    {
        'id': 6,
        'name': 'Tech Compact',
        'description': 'Condensed layout designed specifically for information-heavy technical resumes.',
        'preview': 'tech_compact.jpg'
    },
    {
        'id': 7,
        'name': 'Two Column Minimal',
        'description': 'Modern two-column approach with high scannability and professional flair.',
        'preview': 'two_column.jpg'
    },
    {
        'id': 8,
        'name': 'Premium Dark Mode',
        'description': 'Bold dark theme for a standout digital presence. Modern and high-impact.',
        'preview': 'dark_premium.jpg'
    }
]

@resume_bp.route('/templates')
@login_required
def templates():
    """Template selection page"""
    resume_data = ResumeData.query.filter_by(user_id=current_user.id).first()
    if not resume_data:
        flash('Please fill your details first.', 'warning')
        return redirect(url_for('resume.builder'))
    return render_template('resume_builder/select_template.html', templates=RESUME_TEMPLATES)

@resume_bp.route('/view/<template_id>')
@login_required
def view_resume(template_id):
    """Render resume with specific template"""
    resume_data = ResumeData.query.filter_by(user_id=current_user.id).first()
    if not resume_data:
        flash('Please fill your details first.', 'warning')
        return redirect(url_for('resume.builder'))
        
    template_name = f'resume_builder/templates/template{template_id}.html'
    try:
        return render_template(template_name, data=resume_data)
    except:
        flash('Template not found.', 'danger')
        return redirect(url_for('resume.templates'))

@resume_bp.route('/download/<template_id>')
@login_required
def download_pdf(template_id):
    """
    Redirect to the view page. 
    Downloads are now handled client-side via html2pdf.js for pixel-perfect rendering.
    """
    return redirect(url_for('resume.view_resume', template_id=template_id))
