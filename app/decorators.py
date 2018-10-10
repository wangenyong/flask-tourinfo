from functools import wraps
from flask import g
from .api.errors import permissions

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return permissions('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator