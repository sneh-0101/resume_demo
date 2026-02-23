"""
Resume analysis and matching routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_app import db
from flask_app.models import Resume, Analysis, JobPosting
from flask_app.forms import ResumeUploadForm, JobMatchingForm, QuickAnalysisForm
from flask_app.utils import save_uploaded_file, get_score_color, get_score_label, truncate_text
from flask_app.ai_engine import ResumeParser, NLPProcessor, ResumeMatcher, ReportGenerator
import os

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_resume():
    """Upload resume"""
    form = ResumeUploadForm()
    
    if form.validate_on_submit():
        filename, filepath = save_uploaded_file(form.resume_file.data, current_user.id)
        
        if filename and filepath:
            # Extract text from resume
            try:
                extracted_text = ResumeParser.extract_text_from_pdf(open(filepath, 'rb'))
                
                if not extracted_text:
                    flash('Error extracting text from PDF. Please ensure it\'s a valid PDF.', 'danger')
                    return redirect(url_for('analysis.upload_resume'))
                
                # Extract skills
                extracted_skills = NLPProcessor.extract_skills(extracted_text)
                
                # Save resume to database
                resume = Resume(
                    user_id=current_user.id,
                    filename=form.resume_file.data.filename,
                    filepath=filepath,
                    extracted_text=extracted_text,
                    extracted_skills=extracted_skills
                )
                db.session.add(resume)
                db.session.commit()
                
                flash(f'Resume "{form.resume_file.data.filename}" uploaded successfully!', 'success')
                return redirect(url_for('analysis.resume_list'))
            
            except Exception as e:
                flash(f'Error processing resume: {str(e)}', 'danger')
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    return render_template('analysis/upload.html', form=form)


@analysis_bp.route('/resumes')
@login_required
def resume_list():
    """List user's resumes"""
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
    return render_template('analysis/resume_list.html', resumes=resumes)


@analysis_bp.route('/resume/<resume_id>/delete', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """Delete a resume"""
    resume = Resume.query.get(resume_id)
    
    if not resume or resume.user_id != current_user.id:
        flash('Resume not found', 'danger')
        return redirect(url_for('analysis.resume_list'))
    
    try:
        # Delete file
        if os.path.exists(resume.filepath):
            os.remove(resume.filepath)
        
        # Delete analyses associated with this resume
        Analysis.query.filter_by(resume_id=resume_id).delete()
        
        # Delete resume
        db.session.delete(resume)
        db.session.commit()
        
        flash('Resume deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting resume: {str(e)}', 'danger')
    
    return redirect(url_for('analysis.resume_list'))


@analysis_bp.route('/quick-analysis', methods=['GET', 'POST'])
def quick_analysis():
    """Quick analysis without registration (for demo purposes)"""
    form = QuickAnalysisForm()
    
    if form.validate_on_submit():
        try:
            # Extract text from resume
            resume_file = form.resume_file.data
            extracted_text = ResumeParser.extract_text_from_pdf(resume_file)
            
            if not extracted_text:
                flash('Error extracting text from PDF', 'danger')
                return redirect(url_for('analysis.quick_analysis'))
            
            # Extract skills
            resume_skills = NLPProcessor.extract_skills(extracted_text)
            jd_text = form.job_description.data
            jd_skills = NLPProcessor.extract_skills(jd_text)
            
            # Generate suggestions
            missing_skills = [s for s in jd_skills if s not in resume_skills]
            suggestions = NLPProcessor.generate_suggestions(missing_skills)
            
            # Perform analysis
            analysis_data = ResumeMatcher.analyze_match(
                extracted_text, 
                jd_text, 
                resume_skills, 
                jd_skills
            )
            
            return render_template('analysis/quick_results.html',
                                 score=analysis_data['score'],
                                 matched_skills=analysis_data['matched_skills'],
                                 missing_skills=analysis_data['missing_skills'],
                                 suggestions=suggestions,
                                 ats_findings=analysis_data['ats_findings'],
                                 interview_questions=analysis_data['interview_questions'],
                                 skill_resources=analysis_data['skill_resources'],
                                 match_percentage=analysis_data['match_percentage'],
                                 score_label=get_score_label(analysis_data['score']),
                                 score_color=get_score_color(analysis_data['score']))
        
        except Exception as e:
            flash(f'Error during analysis: {str(e)}', 'danger')
    
    return render_template('analysis/quick_analysis.html', form=form)


@analysis_bp.route('/resume/<resume_id>/analyze', methods=['GET', 'POST'])
@login_required
def analyze_resume(resume_id):
    """Analyze resume against job description"""
    resume = Resume.query.get(resume_id)
    
    if not resume or resume.user_id != current_user.id:
        flash('Resume not found', 'danger')
        return redirect(url_for('analysis.resume_list'))
    
    form = JobMatchingForm()
    
    if form.validate_on_submit():
        try:
            jd_text = form.job_description.data
            resume_text = resume.extracted_text
            resume_skills = resume.extracted_skills
            jd_skills = NLPProcessor.extract_skills(jd_text)
            
            # Perform analysis
            analysis_data = ResumeMatcher.analyze_match(
                resume_text,
                jd_text,
                resume_skills,
                jd_skills
            )
            
            # Generate suggestions
            missing_skills = analysis_data['missing_skills']
            suggestions = NLPProcessor.generate_suggestions(missing_skills)
            
            # Save analysis to database
            analysis = Analysis(
                user_id=current_user.id,
                resume_id=resume_id,
                job_description=jd_text,
                match_score=analysis_data['score'],
                matched_skills=analysis_data['matched_skills'],
                missing_skills=analysis_data['missing_skills'],
                suggestions=suggestions,
                match_percentage=analysis_data['match_percentage'],
                ats_score=analysis_data['ats_score'],
                ats_details={'findings': analysis_data['ats_findings']},
                interview_questions=analysis_data['interview_questions'],
                skill_resources=analysis_data['skill_resources']
            )
            db.session.add(analysis)
            db.session.commit()
            
            flash('Analysis completed successfully!', 'success')
            return redirect(url_for('analysis.view_analysis', analysis_id=analysis.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error during analysis: {str(e)}', 'danger')
    
    return render_template('analysis/analyze.html', form=form, resume=resume)


@analysis_bp.route('/result/<analysis_id>')
@login_required
def view_analysis(analysis_id):
    """View analysis result"""
    analysis = Analysis.query.get(analysis_id)
    
    if not analysis or analysis.user_id != current_user.id:
        flash('Analysis not found', 'danger')
        return redirect(url_for('analysis.resume_list'))
    
    return render_template('analysis/result.html', analysis=analysis,
                         score_label=get_score_label(analysis.match_score),
                         score_color=get_score_color(analysis.match_score))


@analysis_bp.route('/result/<analysis_id>/report')
@login_required
def download_report(analysis_id):
    """Download PDF report"""
    analysis = Analysis.query.get(analysis_id)
    
    if not analysis or analysis.user_id != current_user.id:
        flash('Analysis not found', 'danger')
        return redirect(url_for('analysis.resume_list'))
    
    try:
        resume_name = analysis.resume.filename
        report_buffer = ReportGenerator.generate_report(
            resume_name,
            analysis.match_score,
            analysis.matched_skills,
            analysis.missing_skills,
            analysis.suggestions,
            ats_score=analysis.ats_score,
            ats_findings=analysis.ats_details.get('findings') if analysis.ats_details else None
        )
        
        return send_file(
            report_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_analysis_{analysis.id}.pdf'
        )
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('analysis.view_analysis', analysis_id=analysis_id))


@analysis_bp.route('/history')
@login_required
def history():
    """View analysis history"""
    analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).all()
    return render_template('analysis/history.html', analyses=analyses,
                         score_label_fn=get_score_label,
                         score_color_fn=get_score_color,
                         truncate_fn=truncate_text)
