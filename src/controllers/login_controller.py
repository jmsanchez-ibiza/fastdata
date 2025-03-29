from datetime import datetime
from fasthtml.common import *
from src.auth.login import is_user_logged
# from src.db.DAO_users import UserDAO
from src.views.login_views import login_form

def init_routes(rt):
    LoginController(rt)


class LoginController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()
    
    def init_routes(self):
        self.rt("/login/{errors}")(self.login)
        self.rt("/login_post")(self.login_post)
        self.rt("/logout")(self.logout)

    def login(self, session, request, errors: str = ""):
        return login_form(errors)

    async def login_post(self, session, request):
        user_data = dict(await request.form())
        username = user_data.get("username", "")
        password = user_data.get("password", "")
        next_url = user_data.get("next_url", "/")
        role = user_data.get("user_role", "GENERAL")

        # user_dao = UserDAO()
        # user = user_dao.get_user_by_username(username)
        # # TODO: comprobar el password
        # autenticado = user.check_password(password=password.lower().strip()) if user else False
        autenticado = True
                
        if autenticado:
            # user.last_login = datetime.now()
            # user_dao.update(user)

            # session['user'] = {
            #     "username": user.username,
            #     "password": user.password,
            #     "role": user.role
            # }
            session['user'] = {
                "username": "admin",
                "password": "admin",
                "role": "admin"
            }
            add_toast(session, "Access granted.", "success")
            return RedirectResponse(next_url, status_code=303)
        
        # Not authenticated
        add_toast(session, "Incorrect username or password.", "error")
        return RedirectResponse("/", status_code=303)

    def logout(self, session, request):
        # Delete the user from the session
        if session and is_user_logged(session):
            session.pop('user', None)
        
        # Return to the home page
        add_toast(session, "The session has been closed.", "info")
        return RedirectResponse('/', status_code=303)

