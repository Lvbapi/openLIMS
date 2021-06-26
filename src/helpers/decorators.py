from functools import wraps
import flask_login as login
from flask import url_for
from werkzeug.utils import redirect


def check_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not login.current_user.is_authenticated:
            return redirect(url_for('auth.login_view'))
        return func(*args, **kwargs)

    return decorated_function


def check_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not login.current_user.is_admin():
            return redirect(url_for('site.index'))
        return func(*args, **kwargs)

    return decorated_function


def has_role(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not login.current_user.has_role(role):
                return redirect(url_for('site.index'))
            return func(*args, **kwargs)

        return decorated_function

    return decorator
