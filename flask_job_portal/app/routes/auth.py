"""
Authentication Routes
Handles user registration, login, and logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import db, User

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration route
    Supports three roles: job_seeker, recruiter, admin
    """
    
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        role = request.form.get('role', 'job_seeker')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        company = request.form.get('company')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            flash('All fields are required', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
            company=company if role == 'recruiter' else None
        )
        user.set_password(password)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! Welcome {username}', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route
    Authenticates user and creates session
    """
    
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        # Validate credentials
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been deactivated', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login user
        login_user(user, remember=bool(remember))
        flash(f'Welcome back, {user.username}!', 'success')
        
        # Redirect to appropriate dashboard
        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user.role == 'recruiter':
            return redirect(url_for('recruiter.dashboard'))
        else:
            return redirect(url_for('job_seeker.dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logout route
    Clears user session
    """
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))
