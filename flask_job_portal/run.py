"""
Flask Job Portal - Main Application Entry Point
Run this file to start the development server

Usage:
    python run.py
"""

import os
from app import create_app, db
from app.models import User, Job, Resume, Application

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """
    Add models to Flask shell context
    Useful for database operations in `flask shell`
    """
    return {
        'db': db,
        'User': User,
        'Job': Job,
        'Resume': Resume,
        'Application': Application
    }


if __name__ == '__main__':
    # Create uploads directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run development server
    # Change host to '0.0.0.0' to make it accessible from other machines
    app.run(
        host='127.0.0.1',
        port=5001,  # Using 5001 to avoid conflict with other Flask app
        debug=True
    )
