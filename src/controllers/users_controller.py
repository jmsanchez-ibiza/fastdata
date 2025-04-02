from fasthtml.common import *
from src.core.html_wrappers import *
from src.auth.login import login_required
from src.data.utils import assign_form_data_to_model
from src.data.models import User
from src.data.DAO_users import UserDAO
from src.views.utils import error_msg
# from src.views.users_views import form_usuarios, form_usuarios_confirmacion, lista_usuarios, navbar_botones, users_form
from src.views.users_views import users_form, users_modal_confirmation, users_page

def init_routes(rt):
    UsersController(rt)


class UsersController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/users")(login_required(self.list))
        self.rt("/users_add")(login_required(self.form_add))
        self.rt("/users_edit/{user_id}")(login_required(self.form_edit))
        self.rt("/users_delete/{user_id}")(login_required(self.form_delete))
        self.rt("/users_post")(self.process_post)

    def list(self, session, request):
        try:
            users = UserDAO().get_all(order_by={"username": "ASC"})
            return users_page(session, users)
        except Exception as e:
            return error_msg(f"ERROR: {e}")

    def form_add(self, session, request):
        return users_form(action="add", session=session)

    def form_edit(self, session, request, user_id: int):
        user = UserDAO().get_by_id(user_id)
        if not user:
            return error_msg(f"ERROR: user ID {user_id} not found.")
        return users_form(action="edit", user=user, session=session)

    def form_delete(self, session, request, user_id: int):
        user = UserDAO().get_by_id(user_id)
        if not user:
            return error_msg(f"ERROR: User ID {user_id} was not found.")
        return users_modal_confirmation(action="delete", user=user)

    async def process_post(self, session, request):
        form_data = dict(await request.form())
        action = form_data.get("action", "")
        action2 = form_data.get("action2", "")
        action = action2 if action2 else action
        user_id = int(form_data.get("user_id", 0) or 0)
        user_dao = UserDAO()
        user = None
        errors = {}
        # input(f"DEBUG-INPUT: UsersController:process_post:\n{form_data}\n{action=} {action2=}")

        if action == "add":
            user = User()
            assign_form_data_to_model(user, form_data, exclude_keys=["id"])
            errors = user.validate_data(action, session)

            if not errors:
                user.set_password(user.password)
                user_id, err = user_dao.create(user)
                if not user_id:
                    errors["db"] = f"ERROR-DB: Error creating user: {err}"

        elif action == "edit":
            user = user_dao.get_by_id(user_id)
            if not user:
                return error_msg(f"ERROR: User ID {user_id} not found.")

            assign_form_data_to_model(user, form_data, exclude_keys=["id"])
            errors = user.validate_data(action, session)

            if not errors:
                user.set_password(user.password)
                user_id, err = user_dao.update(user)
                if not user_id:
                    errors["db"] = f"ERROR-DB: Updating the user: {err}"

        elif action == "delete":
            usuario = user_dao.get_by_id(user_id)
            user_id, err = user_dao.delete(user_id)
            if not user_id:
                errors["db"] = f"ERROR-DB: Error al borrar el usuario: {err}"

        elif action == "cancel":
            # Vaciar el contenedor del modal
            return Div(id="user-modals-here")("")
        
        if errors:
            user = user or User()
            return users_form(session=session, action=action, user=user, errors=errors)

        users = user_dao.get_all(order_by={"username": "ASC"})
        return users_page(session=session, users=users, user_id=user_id, hx_swap_oob=True)


