"""
Utility functions for the application
"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file, user_id):
    """
    Save uploaded file to disk with unique naming.
    
    Args:
        file: FileStorage object from Flask
        user_id: User ID for organizing uploads
        
    Returns:
        tuple: (filename, filepath) or (None, None) if error
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add UUID to ensure uniqueness
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Create user upload directory if it doesn't exist
        user_upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], user_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        
        filepath = os.path.join(user_upload_dir, unique_filename)
        file.save(filepath)
        
        return unique_filename, filepath
    
    return None, None


def delete_file(filepath):
    """Safely delete a file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False


def format_percentage(value):
    """Format percentage with proper rounding"""
    return round(value, 2)


def get_score_color(score):
    """Get Bootstrap color class based on score"""
    if score >= 75:
        return 'success'
    elif score >= 50:
        return 'warning'
    else:
        return 'danger'


def get_score_label(score):
    """Get human-readable label for score"""
    if score >= 75:
        return 'Excellent Match'
    elif score >= 60:
        return 'Good Match'
    elif score >= 40:
        return 'Partial Match'
    else:
        return 'Poor Match'


def truncate_text(text, max_length=100):
    """Truncate text to max length with ellipsis"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text
