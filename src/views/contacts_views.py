from fasthtml.common import *
from src.core.html_wrappers import *
from src.data.DAO_contacts import ContactDAO
from src.data.models import Contact, Client
from src.views.components.buttons import rowButton
from src.views.components.forms import mk_input


def contacts_form(session={}, action: str = "edit", contact: Contact = None, client: Client = None, errors: dict = {}):
    if action == "add" and not errors:
        contact = Contact()

    texto_boton_accion = "Add" if action == "add" else "Save"

    form = Form(id="contact-details-form")(
        Input(name="action", type="hidden", value=action),
        Input(name="contact_id", type="hidden", value=contact.id if contact else 0),
        Input(name="client_id", type="hidden", value=contact.client.id if contact else 0),

        Div(cls="row")(
            Div(cls="form-group col-md-12")(
                mk_input(id="contact_name", placeholder="Contact name", value=contact.contact_name if contact else "", errors=errors, autofocus=True),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="phone", placeholder="Phone", value=contact.phone if contact else "", errors=errors),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="mobile", placeholder="Mobile", value=contact.mobile if contact else "", errors=errors),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-12")(
                mk_input(id="email", placeholder="Email", value=contact.email if contact else "", errors=errors),
            ),
        ),

        Div(cls="form-group")(
            mk_input(id="notes", placeholder="Notas", value=contact.notes if contact else "", errors=errors),
        ),

        Div(cls="row")(
            Div(cls="d-flex justify-content-end")(
                Button(
                    cls="btn btn-secondary px-2 my-2 mx-1",
                    type="button",
                    hx_post="/contacts_post",
                    hx_target="#contact-modals-here",
                    hx_vals={"action2": "cancel"},
                )("Cancel"),

                Button(
                    cls="btn btn-primary px-4 my-2 mx-1",
                    type='button',
                    hx_post="/contacts_post",
                    hx_target="#contact-modals-here",
                    hx_indicator="#spinner",
                )(
                    Div(cls="d-flex align-items-center gap-2")(
                        texto_boton_accion,
                        Img(
                            id="spinner",
                            cls="my-indicator align-self-center",  # Alineación vertical
                            src="img/ring-spinner.svg",
                            style="height: 1.5em;"  # Alineado con el tamaño del texto
                        ),
                    ),
                )
            ),
        ),
    )

    header_title = Div(
            H3("NEW contact:"),
            H4("Client: ", Span(cls="text-primary fw-bold")(f"{client.id}/{client.clcomer}")) if client else "",
        ) if action == "add" else Div(
                                    H3("Contact: ", Span(cls="text-primary fw-bold")(f"{contact.id}/{contact.contact_name}")),
                                    H4("Client: ", Span(cls="text-primary fw-bold")(f"{client.id}/{client.clcomer}")) if client else "",
                                )

    return Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True)(
            Div(cls="boot-modal-header")(
                Div(cls="d-flex justify-content-between m-3")(
                    header_title,
                    Button(cls="btn-close", type="button", hx_post="/contacts_post", hx_target="#contact-modals-here", hx_vals={"accion2": "cancel"}),
                ),
            ),
            Div(cls="boot-modal-body")(
                form,
            )
        )
    )

def contacts_modal_confirmation(contact: Contact = None, action: str = "", errors: dict = {}):
    hx_vals_dict = {'action': 'delete', 'contact_id': contact.id if contact else 0}
    return Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True, style="width: 50%;")(
            Div(cls="boot-modal-header")(
                Div(cls="m-3")(H3("Contact DELETE")),
            ),
            Form()(
                Div(cls="boot-modal-body")(
                    Input(name="action", type="hidden", value=action),
                    Input(name="contact_id", type="hidden", value=contact.id if contact else 0),
                    Input(name="client_id", type="hidden", value=contact.client.id if contact else 0),
                    Div(cls="m-10")(
                        Span(cls="btn btn-danger fs-3")(errors["db"]) if "db" in errors else "",
                        H5("Are you sure you want to DELETE this contact?") if "db" not in errors else "",
                        H5(f"{contact.id}/{contact.contact_name}"),
                    ),
                ),
                Div(cls="d-flex justify-content-end boot-modal-footer")(
                    Button(
                        cls="btn btn-secondary px-2 my-2 mx-1",
                        type="button",
                        hx_post="/contacts_post",
                        hx_target="#contact-modals-here",
                        hx_vals={"action2": "cancel"},
                    )("Cancel"),
                    Button(
                        cls="btn btn-danger px-4 my-2 mx-1",
                        type='button',
                        hx_post="/contacts_post",
                        hx_target="#contact-modals-here",
                        hx_vals=hx_vals_dict,
                    )("Delete") if "db" not in errors else "",
                )
            )
        )
    )

def contact_row(session, contact: Contact, contact_id: int = 0):
    highlighted_cls = "highlighted" if contact.id == contact_id else ""
    highlighted_style = "background: rgb(255, 190, 190, 1);" if contact.id == contact_id else ""

    return Tr(id=f"id-{contact.id}", cls=highlighted_cls)(
        Td(cls="d-flex justify-content-right btn-group-horizontal", style=highlighted_style)(
            rowButton("edit", url=f"/contacts_edit/{contact.id}", target="contact-modals-here", icon="bi-pencil-square", color="primary"),
            rowButton("delete", url=f"/contacts_delete/{contact.id}", target="contact-modals-here", icon="bi-trash", color="danger"),
        ),
        Td(style=highlighted_style)(f"{contact.id:03}"),
        Td(style=highlighted_style)(contact.contact_name),
    )

def contacts_navbar(session, client_id: int = 0):
    return Div(
        Nav(
            cls="d-flex justify-content-start p-2 rounded gap-3",
            style="background-color: #002db3; color: white;",
            force_cls=False,
            force_style=True,
        )(
            H5("Contact's Table"),
            Button(
                cls="btn btn-primary",
                hx_get="/contacts_add",
                hx_trigger="click",
                hx_target="#contact-modals-here",
                hx_vals={"client_id": client_id},
            )(
                I(cls="bi-plus-circle text-white fs-5"),
                Span(cls="mx-1")("Add"),
            ),
            Button(cls="btn btn-primary disabled")(
                I(cls="bi-printer text-white fs-5"), Span(cls="mx-1")("Reports")
            ),
            Button(cls="btn btn-primary disabled")(
                I(cls="bi-folder-symlink text-white fs-5"), Span(cls="mx-1")("Export")
            ),
        )
    )

def contacts_list(session, contacts, contact_id: int = 0):
    return Table(
        id="contacts-table",
        data_page_length="10",
        cls="table table-striped table-hover display compact datatable",
        style="width: 100%; background-color: white;",
    )(
        Thead(
            Tr(
                Th(scope="col")("🛠️"),
                Th(scope="col")("ID"),
                Th(scope="col")("Nombre"),
            )
        ),
        Tbody()(
            *[contact_row(session, contact, contact_id=contact_id) for contact in contacts]
                if contacts else Tr(Td("No contacts found")),
         ),
        Tfoot(
            Tr(
                Th(scope="col", cls="dt-orderable-asc")("🛠️"),
                Th(scope="col", cls="dt-orderable-asc")("ID"),
                Th(scope="col", cls="dt-orderable-asc")("Nombre"),
            )
        ),
    ) if contacts else Div(H5(cls="text-center text-danger pt-3")("No contacts found"))

def contacts_page(session, contacts=None, client_id: int = 0, contact_id:int=0, hx_swap_oob: bool = False):
    # Load contacts
    contacts = contacts or ContactDAO().get_all(order_by={"contact_name": "ASC"}) if not client_id else ContactDAO().get_all_by_client_id(client_id)

    return Div(
        contacts_navbar(session, client_id=client_id),
        Div(id="contact-modals-here", hx_swap_oob="true" if hx_swap_oob else "")(""),
        Div(id="contacts-list", hx_swap_oob="true" if hx_swap_oob else "")(
            contacts_list(session, contacts, contact_id=contact_id),
        )
    )

