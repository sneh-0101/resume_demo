"""
Authentication routes
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_app import db
from flask_app.models import User
from flask_app.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Validate admin code if admin role selected
        if form.role.data == 'admin':
            from flask import current_app
            if form.admin_code.data != current_app.config['ADMIN_SECRET_CODE']:
                flash('Invalid admin secret code. Please contact the administrator.', 'danger')
                return redirect(url_for('auth.register'))
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data or '',
            last_name=form.last_name.data or '',
            role=form.role.data,
            is_admin=(form.role.data == 'admin')
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! Welcome, {user.username}! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=True)
        next_page = request.args.get('next')
        
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
