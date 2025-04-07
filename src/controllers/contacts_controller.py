# Contact's controller
from fasthtml.common import *
from src.core.html_wrappers import *
from src.auth.login import login_required
from src.data.utils import assign_form_data_to_model
from src.data.models import Contact
from src.data.DAO_clients import ClientDAO
from src.data.DAO_contacts import ContactDAO
from src.views.contacts_views import contacts_form, contacts_modal_confirmation, contacts_page
from src.views.utils import error_msg

def init_routes(rt):
    ContactsController(rt)

class ContactsController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        # Define the routes for the contacts controller
        self.rt("/contacts")(login_required(self.list))
        self.rt("/contacts_add")(login_required(self.form_add))
        self.rt("/contacts_edit/{contact_id}")(login_required(self.form_edit))
        self.rt("/contacts_delete/{contact_id}")(login_required(self.form_delete))
        self.rt("/contacts_post")(self.process_post)

    def list(self, session, request):
        # Not implemented because the contact list is retrieved on the client page
        pass

    def form_add(self, session, request):
        client_id = int(request.query_params.get("client_id", 0) or 0)
        if client_id:
            client = ClientDAO().get_by_id(client_id)

        return contacts_form(action="add", session=session, client=client)

    def form_edit(self, session, request, contact_id: int):
        contact = ContactDAO().get_by_id(contact_id)
        if not contact:
            return error_msg(f"ERROR: Contact ID {contact_id} not found.")
        return contacts_form(action="edit", contact=contact, session=session)

    def form_delete(self, session, request, contact_id: int):
        """Form to confirm deletion of a contact"""
        contact = ContactDAO().get_by_id(contact_id)
        if not contact:
            return error_msg(f"ERROR: Contact ID {contact_id} not found.")
        return contacts_modal_confirmation(action="delete", contact=contact)

    async def process_post(self, session, request):
        form_data = dict(await request.form())
        action = form_data.get("action", "")
        action2 = form_data.get("action2", "")
        action = action2 if action2 else action
        client_id = int(form_data.get("client_id", 0) or 0)
        contact_id = int(form_data.get("contact_id", 0) or 0)
        contact_dao = ContactDAO()
        contact = contact_dao.get_by_id(contact_id) if contact_id else None
        client = ClientDAO().get_by_id(client_id) if client_id else None
        errors = {}

        if action == "add":
            contact = Contact()
            assign_form_data_to_model(contact, form_data, exclude_keys=["id"])
            contact.id_client = client_id  # Assign client_id to contact
            errors = contact.validate(action, session)
            if not errors:
                contact_id, err = contact_dao.create(contact)
                if not contact_id:
                    errors["db"] = f"ERROR-DB: Creating contact: {err}"

        elif action == "edit":
            if not contact:
                return error_msg(f"ERROR: Contact ID {contact_id} not found.")
            assign_form_data_to_model(contact, form_data, exclude_keys=["id"])
            errors = contact.validate(action, session)
            if not errors:
                contact_id, err = contact_dao.update(contact)
                if not contact_id:
                    errors["db"] = f"ERROR-DB: Updating contact: {err}"

        elif action == "delete":
            contact_id, err = contact_dao.delete(contact_id)
            if not contact_id:
                errors["db"] = f"ERROR-DB: Deleting contact: {err}"

        # If action2 had been "cancel", we would have already gotten here

        if errors:
            contact = contact or Contact()
            return contacts_form(session=session, action=action, contact=contact, client=client, errors=errors)

        contacts = ContactDAO().get_all(order_by={"contact_name": "ASC"}) if not client_id else ContactDAO().get_all_by_client_id(client_id)
        return contacts_page(session=session, contacts=contacts, contact_id=contact_id, client_id=client_id, hx_swap_oob=True)

