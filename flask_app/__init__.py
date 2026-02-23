"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuration
    if config_name == 'production':
        app.config.from_object('flask_app.config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('flask_app.config.TestingConfig')
    else:
        app.config.from_object('flask_app.config.DevelopmentConfig')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.remember_cookie_duration = timedelta(days=7)
    
    # Create instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Register blueprints
    from flask_app.routes.auth import auth_bp
    from flask_app.routes.main import main_bp
    from flask_app.routes.dashboard import dashboard_bp
    from flask_app.routes.analysis import analysis_bp
    from flask_app.routes.admin import admin_bp
    from flask_app.routes.hr import hr_bp
    from flask_app.routes.resume import resume_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(resume_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
