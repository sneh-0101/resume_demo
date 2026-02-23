"""
Main Flask application entry point
Run with: python run.py
"""

import os
from flask_app import create_app, db, login_manager
from flask_app.models import User

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(user_id)


@app.shell_context_processor
def make_shell_context():
    """Make database objects available in shell"""
    return {'db': db, 'User': User}


@app.before_request
def before_request():
    """Set permanent session"""
    from flask import session
    session.permanent = True
    app.permanent_session_lifetime.total_seconds()


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the development server
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
