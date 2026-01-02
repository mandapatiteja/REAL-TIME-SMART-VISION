"""
Authentication Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models.auth_service import create_user, authenticate_user, get_user_by_id

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    '''Login page and authentication'''
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please provide both email and password', 'error')
            return render_template('login.html')
        
        user = authenticate_user(email, password)
        
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            
            # Show login success popup on login page, then redirect via JS
            next_page = request.args.get('next') or url_for('main.dashboard')
            flash('Login successful', 'login_success')
            return render_template('login.html', active_tab='login', next_page=next_page)
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', active_tab='login')

@bp.route('/guest-login')
def guest_login():
    '''Login as guest user'''
    session['user_id'] = 'guest'
    session['user_email'] = 'guest@example.com'
    session['user_name'] = 'Guest User'
    
    flash('Logged in as guest', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    '''Registration page and user creation'''
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        name = request.form.get('name', '').strip()
        
        # Validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html', active_tab='signup')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('login.html', active_tab='signup')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('login.html', active_tab='signup')
        
        user = create_user(email, password, name)
        
        if user:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already exists. Please login instead.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html', active_tab='signup')

@bp.route('/logout')
def logout():
    '''Logout user'''
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('main.welcome'))

def login_required(f):
    '''Decorator to protect routes that require authentication'''
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function





