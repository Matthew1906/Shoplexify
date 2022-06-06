from flask import abort
from flask_login import current_user
from functools import wraps

def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.id == 1 :
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function

def member_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.id != 1 :
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function
    