from flask import Blueprint, render_template, session, redirect, url_for, flash, request, send_from_directory
from functools import wraps

bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
def welcome():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('welcome.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@bp.route('/results')
@login_required
def results():
    return render_template('results.html')

@bp.route('/history')
@login_required
def history():
    return render_template('history.html')

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
