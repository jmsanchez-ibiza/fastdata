from fasthtml.common import *
from functools import wraps
# from urllib.parse import urlencode
from starlette.requests import Request
from src.utils.js_scripts import auto_destroy_js

def _get_arguments(*args):
    # args, can be <starlette.requests.Request> or a dict -> session
    user = None
    session = {}
    request = None
    if len(args) > 1:
        # args has 1 or 2 arguments
        if isinstance(args[0], dict): session = args[0]
        if isinstance(args[1], dict): session = args[1]
        if isinstance(args[0], Request): request = args[0]
        if isinstance(args[1], Request): request = args[1]
        
    if session and "user" in session:
        user = session.get("user", None)
    return session, request, user

def login_required(func):
    """ Decorator to restrict access to authenticated users only """
    @wraps(func)
    def wrapper(*args, **kwargs):
        session, request, user = _get_arguments(*args)
        if not user:
            # next_url = request.url.path  # Capturar la URL actual
            # redir_url = f"{login_redir}?{urlencode({'next': next_url})}"
            add_toast(session, "To access this page, you must log in.", "error")
            return RedirectResponse("/", status_code=303)

        request.scope['user'] = user  # Pass the user to the request
        return func(*args, **kwargs)  # Call the original function with its original arguments
    return wrapper

def user_role_required(required_role: str = ""):
    """ Decorator to restrict access by roles """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session, request, user = _get_arguments(*args)
            
            if not user:
                # next_url = request.url.path  # Capturar la URL actual
                # redir_url = f"{login_redir}?{urlencode({'next': next_url})}"
                return RedirectResponse("/", status_code=303)

            if 'role' in user and user['role'].lower().strip() != required_role.lower().strip():
                return Div(cls="d-flex justify-content-center")(
                    H3(cls="auto-destroy btn btn-danger")(
                        "NO tiene acceso a esta opción"
                    ),
                    auto_destroy_js(segundos=2),
                )

            request.scope['user'] = user  # Pass the user to the request
            return func(*args, **kwargs)  # Call the original function with its original arguments
        return wrapper
    return decorator

# Check if we are logged in; user_logged is not empty
def is_user_logged(session):
    return True if isinstance(session, dict) and 'user' in session and session['user'] else False

# Get information of the logged-in user
def get_user_info(session):
    ret_dict = session['user'] if 'user' in session else {}
    return ret_dict

# Check if the user is 'ADMIN'
def is_user_admin(session):
    role = get_user_info(session)
    return role['role'].lower() == "admin"
