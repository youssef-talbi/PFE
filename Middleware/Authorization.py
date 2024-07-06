from functools import wraps
from flask import session, redirect, url_for, abort

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session:
            return redirect(url_for('auth.login'))  # Redirect to login
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role_name').lower() != 'hr administrator':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
