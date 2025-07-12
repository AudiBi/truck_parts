from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user


def login_required_custom(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def role_requis(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role.nom.lower() != role.lower():
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


