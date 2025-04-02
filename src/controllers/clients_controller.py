# Client's controller
from fasthtml.common import *
from src.core.html_wrappers import *
from src.auth.login import login_required
from src.data.utils import assign_form_data_to_model
from src.data.models import Client
from src.data.DAO_clients import ClientDAO
from src.views.utils import error_msg
from src.views.clients_views import clients_form, clients_modal_confirmation, clients_page

def init_routes(rt):
    ClientsController(rt)

class ClientsController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/clients")(login_required(self.list))
        self.rt("/clients_add")(login_required(self.form_add))
        self.rt("/clients_edit/{client_id}")(login_required(self.form_edit))
        self.rt("/clients_delete/{client_id}")(login_required(self.form_delete))
        self.rt("/clients_post")(self.process_post)

    def list(self, session, request):
        try:
            clients = ClientDAO().get_all(order_by={"clcomer": "ASC"})
            return clients_page(session, clients)
        except Exception as e:
            return error_msg(f"ERROR: {e}")

    def form_add(self, session, request):
        return clients_form(action="add", session=session)

    def form_edit(self, session, request, client_id: int):
        client = ClientDAO().get_by_id(client_id)
        if not client:
            return error_msg(f"ERROR: Client ID {client_id} not found.")
        return clients_form(action="edit", client=client, session=session)

    def form_delete(self, session, request, client_id: int):
        client = ClientDAO().get_by_id(client_id)
        if not client:
            return error_msg(f"ERROR: Client ID {client_id} not found.")
        return clients_modal_confirmation(action="delete", client=client)

    async def process_post(self, session, request):
        form_data = dict(await request.form())
        action = form_data.get("action", "")
        action2 = form_data.get("action2", "")
        action = action2 if action2 else action
        client_id = int(form_data.get("client_id", 0) or 0)
        client_dao = ClientDAO()
        client = None
        errors = {}

        if action == "add":
            client = Client()
            assign_form_data_to_model(client, form_data, exclude_keys=["id"])
            errors = client.validate(action, session)
            if not errors:
                client_id, err = client_dao.create(client)
                if not client_id:
                    errors["db"] = f"ERROR-DB: Creating client: {err}"

        elif action == "edit":
            client = client_dao.get_by_id(client_id)
            if not client:
                return error_msg(f"ERROR: Client ID {client_id} not found.")
            assign_form_data_to_model(client, form_data, exclude_keys=["id"])
            errors = client.validate(action, session)
            if not errors:
                client_id, err = client_dao.update(client)
                if not client_id:
                    errors["db"] = f"ERROR-DB: Updating client: {err}"

        elif action == "delete":
            client_id, err = client_dao.delete(client_id)
            if not client_id:
                errors["db"] = f"ERROR-DB: Deleting client: {err}"

        elif action == "cancel":
            return Div(id="client-modals-here")("")

        if errors:
            client = client or Client()
            return clients_form(session=session, action=action, client=client, errors=errors)

        clients = client_dao.get_all(order_by={"clcomer": "ASC"})
        return clients_page(session=session, clients=clients, client_id=client_id, hx_swap_oob=True)
