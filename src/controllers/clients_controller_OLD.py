from fasthtml.common import *
from src.mycore.html_wrappers import *
from src.db.DAO_clientes_contactos import ClienteContactoDAO
from src.db.models import Cliente, ClienteContacto
from src.db.utils import assign_form_data_to_model
from src.auth.login import login_required, user_role_required
from src.db.DAO_clientes import ClienteDAO
from src.views.clientes_contactos_views import form_clt_contactos_confirmacion, form_contactos, rowContacto
from src.views.components.layout import search_input
from src.views.components.tablas import ClientesTablaView, ContactosTablaView
from src.views.utils import error_msg
from src.views.clientes_views import navbar_botones, form_clientes, form_clientes_confirmacion, rowCliente
from src.scripts import scroll_into_obj

def init_routes(rt):
    ClientesController(rt)
    ClienteContactosController(rt)

class ClientesController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/clt")(login_required(self.listar))
        self.rt("/clt_crear")(login_required(user_role_required("admin")(self.form_crear)))
        self.rt("/clt_editar/{cliente_id}")(login_required(self.form_editar))
        self.rt("/clt_borrar/{cliente_id}")(login_required(self.form_borrar))
        self.rt("/clt_post")(self.procesar_post)
        self.rt("/clt_filtrar")(self.filtrar)

    def listar(self, session, request):
        dao = ClienteDAO()
        clientes = dao.get_all(cargar_relaciones=True, order_by={"id": "ASC", "clcomer": "ASC"})
        return Div(cls="table-responsive p-1")(
            navbar_botones(),
            Div(id="clt-modals-here"),
            Div(id="lista-clientes")(
                ClientesTablaView(clientes, row_func=rowCliente).render(),
            )
        )

    def form_crear(self, session, request):
        return form_clientes(accion="crear")

    def form_editar(self, session, request, cliente_id: int):
        cliente = ClienteDAO().get_by_id(cliente_id, cargar_relaciones=True)
        if not cliente:
            return error_msg(f"ERROR: Cliente ID {cliente_id} no encontrado.")
        return form_clientes(accion="editar", cliente=cliente)

    def form_borrar(self, session, request, cliente_id: int):
        cliente = ClienteDAO().get_by_id(cliente_id, cargar_relaciones=True)
        if not cliente:
            return error_msg(f"ERROR: Cliente ID {cliente_id} no encontrado.")
        if not cliente.can_delete:
            return form_clientes_confirmacion(accion="borrar", cliente=cliente,
                errors={"db": "No se puede borrar el cliente, tiene contactos asociados."})
        return form_clientes_confirmacion(accion="borrar", cliente=cliente)

    async def procesar_post(self, session, request):
        form_data = dict(await request.form())

        accion = form_data.get("accion", "")
        accion2 = form_data.get("accion2", "")
        accion = accion2 if accion2 else accion

        cliente_id = int(form_data.get("id", 0) or 0)
        dao = ClienteDAO()
        cliente = None
        errors = {}

        # input(f"DEBUG-PAUSE: clt_post:procesar_post\n{form_data=}\n{cliente_id=}")
        
        if accion == "crear":
            cliente = Cliente()
            assign_form_data_to_model(cliente, form_data, exclude_keys=["id"])
            errors = cliente.validar_registro(accion, session)
            if not errors:
                cliente_id, err = dao.create(cliente)
                if not cliente_id:
                    errors["db"] = f"ERROR-DB: Error al crear cliente: {err}"

        elif accion == "editar":
            cliente = dao.get_by_id(cliente_id, cargar_relaciones=True)
            if not cliente:
                return error_msg(f"ERROR: Cliente con ID {cliente_id} no encontrado.")
            assign_form_data_to_model(cliente, form_data, exclude_keys=["id"])
            errors = cliente.validar_registro(accion, session)
            if not errors:
                cliente_id, err = dao.update(cliente)
                if not cliente_id:
                    errors["db"] = f"ERROR-DB: Error al actualizar cliente: {err}"

        elif accion == "borrar":
            cliente = dao.get_by_id(cliente_id, cargar_relaciones=True)
            cliente_id, err = dao.delete(cliente_id)
            if not cliente_id:
                errors["db"] = f"ERROR-DB: Error al borrar cliente: {err}"

        if errors:
            cliente = cliente or Cliente()
            return form_clientes(cliente=cliente, accion=accion, errors=errors)

        # Actualizar lista
        clientes = dao.get_all(cargar_relaciones=True, order_by={"id": "ASC"})

        return Div(
            Div(P(""), id="clt-modals-here"),
            Div(id="lista-clientes", hx_swap_oob="true")(
                ClientesTablaView(clientes, row_func=rowCliente, row_kwargs={"cliente_id": cliente_id}).render(),
                scroll_into_obj(f"id-{cliente_id}"),
            ),
            search_input(
                tabla="clientes",
                ruta="clt_filtrar",
                target="lista-clientes",
                swap_oob=True
            ),
        )

    def filtrar(self, session, request):
        query = request.query_params.get("query", "").lower()
        dao = ClienteDAO()
        clientes = dao.get_all(cargar_relaciones=True, order_by={"id": "ASC", "clcomer": "ASC"})

        if query:
            if query.isdigit():  # Verifica si el query son dígitos
                clientes = [
                    c for c in clientes
                    if str(c.id) == query
                    or query in (c.clname or "").lower()
                    or query in (c.clcomer or "").lower()
                ]
            else:
                clientes = [
                    c for c in clientes
                    if query in (c.clname or "").lower() or query in (c.clcomer or "").lower()
                ]

        return ClientesTablaView(clientes, row_func=rowCliente).render()


class ClienteContactosController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/clt_contacto_crear/{cliente_id}")(login_required(self.form_crear))
        self.rt("/clt_contacto_editar/{contacto_id}")(login_required(self.form_editar))
        self.rt("/clt_contacto_borrar/{contacto_id}")(login_required(self.form_borrar))
        self.rt("/clt_contacto_post")(self.procesar_post)

    def form_crear(self, session, request, cliente_id: int):
        cliente = ClienteDAO().get_by_id(cliente_id, cargar_relaciones=True)
        if not cliente:
            return error_msg(f"ERROR: Cliente ID {cliente_id} no encontrado.")
        return form_contactos(cliente=cliente, accion="crear")

    def form_editar(self, session, request, contacto_id: int):
        contacto = ClienteContactoDAO().get_by_id(contacto_id, cargar_relaciones=True)
        if not contacto:
            return error_msg(f"ERROR: Contacto ID {contacto_id} no encontrado.")
        return form_contactos(contacto=contacto, accion="editar")

    def form_borrar(self, session, request, contacto_id: int):
        contacto = ClienteContactoDAO().get_by_id(contacto_id, cargar_relaciones=True)
        if not contacto:
            return error_msg(f"ERROR: Contacto ID {contacto_id} no encontrado.")
        return form_clt_contactos_confirmacion(contacto=contacto, accion="borrar")

    async def procesar_post(self, session, request):
        form_data = dict(await request.form())
        accion = form_data.get("accion", "")
        accion2 = form_data.get("accion2", "")
        accion = accion2 if accion2 else accion

        cliente_id = int(form_data.get("id_cliente", 0) or 0)
        contacto_id = int(form_data.get("contacto_id", 0) or 0)

        cliente = ClienteDAO().get_by_id(cliente_id, cargar_relaciones=True)
        contacto_dao = ClienteContactoDAO()
        contacto = None
        errors = {}

        if accion == "crear":
            contacto = ClienteContacto()
            assign_form_data_to_model(contacto, form_data, exclude_keys=["id"])
            errors = contacto.validar_registro(accion, session)
            if not errors:
                contacto_id, err = contacto_dao.create(contacto)
                if not contacto_id:
                    errors["db"] = f"ERROR-DB: Error al crear contacto: {err}"

        elif accion == "editar":
            contacto = contacto_dao.get_by_id(contacto_id, cargar_relaciones=True)
            if not contacto:
                return error_msg(f"ERROR: Contacto ID {contacto_id} no encontrado.")
            assign_form_data_to_model(contacto, form_data, exclude_keys=["id"])
            errors = contacto.validar_registro(accion, session)
            if not errors:
                contacto_id, err = contacto_dao.update(contacto)
                if not contacto_id:
                    errors["db"] = f"ERROR-DB: Error al actualizar contacto: {err}"

        elif accion == "borrar":
            contacto = contacto_dao.get_by_id(contacto_id, cargar_relaciones=True)
            contacto_id, err = contacto_dao.delete(contacto_id)
            if not contacto_id:
                errors["db"] = f"ERROR-DB: Error al borrar contacto: {err}"

        if errors:
            contacto = contacto or ClienteContacto()
            return form_contactos(cliente=cliente, contacto=contacto, accion=accion, errors=errors)

        # Actualizar tabla
        contactos = contacto_dao.get_all(filtro={"id_cliente": cliente_id})
        return Div(
            Div(id="contacto-modals-here"),
            Div(id="lista-contactos", hx_swap_oob="true")(
                ContactosTablaView(contactos, row_func=rowContacto, row_kwargs={"contacto_id": contacto_id}).render(),
            )
        )


