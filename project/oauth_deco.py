from flask import session, request, current_app
from flask_login.config import EXEMPT_METHODS
from functools import wraps
from werkzeug.local import LocalProxy
from flask import (_request_ctx_stack, current_app, request, session, url_for,
                   has_request_context)

def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()

def login_fresh():
    '''
    This returns ``True`` if the current login is fresh.
    '''
    return session.get('_fresh', False)
    
current_user = LocalProxy(lambda: _get_user())

def login_is_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if request.method in EXEMPT_METHODS:
            return f(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return f(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not login_fresh():
            return current_app.login_manager.needs_refresh()
        elif user:
            return f(*args, **kwargs)
        return f(*args, **kwargs)
    return decorated_function