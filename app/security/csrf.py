from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask import session

# Initialize CSRF protection
csrf_protection = CSRFProtect()


def init_csrf_tokens():
    """Initialize CSRF token in session if not already present"""
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf()
