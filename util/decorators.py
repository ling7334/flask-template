from flask import g, abort

def user_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if "user" not in g:
            abort(401)
        return f(*args, **kwargs)
    return decorator

def admin_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if "user" not in g:
            abort(401)
        if not g.user.admin:
            abort(403)
        return f(*args, **kwargs)
    return decorator
