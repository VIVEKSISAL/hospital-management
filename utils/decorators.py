"""
Custom decorators for authorization and authentication
"""
from functools import wraps
from flask import redirect, url_for, render_template
from flask_login import current_user

def anonymous_required(f):
    """Decorator to ensure user is not logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            if not any(current_user.role == role for role in roles):
                return render_template('errors/403.html'), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            return render_template('errors/403.html'), 403
        
        return f(*args, **kwargs)
    return decorated_function
