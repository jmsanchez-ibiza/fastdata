from fasthtml.common import *
from src.core.html_wrappers import *
from src.auth.login import login_required
from src.data.utils import assign_form_data_to_model
from src.data.models import User
from src.data.DAO_users import UserDAO
from src.views.utils import error_msg
# from src.views.users_views import form_usuarios, form_usuarios_confirmacion, lista_usuarios, navbar_botones, users_form
from src.views.users_views import users_modal_confirmation, users_page

def init_routes(rt):
    UsersController(rt)


class UsersController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/users")(login_required(self.list))
        # self.rt("/users_add")(login_required(self.form_add))
        # self.rt("/users_edit/{user_id}")(login_required(self.form_edit))
        self.rt("/users_delete/{user_id}")(login_required(self.form_delete))
        # self.rt("/users_post")(self.procesar_post)

    def list(self, session, request):
        try:
            users = UserDAO().get_all(order_by={"username": "ASC"})
            return users_page(session, users)
        # Div(cls="table-responsive p-1")(
        #         navbar_botones(),
        #         Div(id="usuario-modals-here"),
        #         Div(id="lista-users")(lista_usuarios(users))
        #     )
        except Exception as e:
            return error_msg(f"ERROR: {e}")

    def form_crear(self, session, request):
        return form_usuarios(accion="crear", session=session)

    def form_editar(self, session, request, user_id: int):
        usuario = UserDAO().get_by_id(user_id)
        if not usuario:
            return error_msg(f"ERROR: Usuario ID {user_id} no encontrado.")
        return form_usuarios(accion="editar", usuario=usuario, session=session)

    def form_delete(self, session, request, user_id: int):
        user = UserDAO().get_by_id(user_id)
        if not user:
            return error_msg(f"ERROR: User ID {user_id} was not found.")
        return users_modal_confirmation(action="delete", user=user)

    async def procesar_post(self, session, request):
        form_data = dict(await request.form())
        accion = form_data.get("accion", "")
        accion2 = form_data.get("accion2", "")
        accion = accion2 if accion2 else accion
        user_id = int(form_data.get("id", 0) or 0)

        user_dao = UserDAO()
        usuario = None
        errors = {}

        if accion == "crear":
            usuario = User()
            assign_form_data_to_model(usuario, form_data, exclude_keys=["id"])
            errors = usuario.validar_registro(accion, session)

            if not errors:
                usuario.set_password(usuario.password)
                user_id, err = user_dao.create(usuario)
                if not user_id:
                    errors["db"] = f"ERROR-DB: Error al crear usuario: {err}"

        elif accion == "editar":
            usuario = user_dao.get_by_id(user_id)
            if not usuario:
                return error_msg(f"ERROR: Usuario con ID {user_id} no encontrado.")

            assign_form_data_to_model(usuario, form_data, exclude_keys=["id"])
            errors = usuario.validar_registro(accion, session)

            if not errors:
                usuario.set_password(usuario.password)
                user_id, err = user_dao.update(usuario)
                if not user_id:
                    errors["db"] = f"ERROR-DB: Error al actualizar el usuario: {err}"

        elif accion == "borrar":
            usuario = user_dao.get_by_id(user_id)
            user_id, err = user_dao.delete(user_id)
            if not user_id:
                errors["db"] = f"ERROR-DB: Error al borrar el usuario: {err}"

        if errors:
            usuario = usuario or User()
            return form_usuarios(usuario=usuario, accion=accion, errors=errors, session=session)

        usuarios = user_dao.get_all(order_by={"username": "ASC"})
        return Div(
            Div(P(""), id="usuario-modals-here"),
            Div(id="lista-usuarios", hx_swap_oob="true")(
                lista_usuarios(usuarios, user_id=user_id)
            )
        )

