from fasthtml.common import *
from src.core.html_wrappers import *
from src.data.models import Client
from src.views.components.buttons import rowButton
from src.views.components.forms import mk_input

def clients_form(session={}, action: str = "edit", client: Client = None, errors: dict = {}):
    if action == "add" and not errors:
        client = Client()

    texto_boton_accion = "Add" if action == "add" else "Save"

    form = Form(id="client-details-form")(
        Input(name="action", type="hidden", value=action),
        Input(name="client_id", type="hidden", value=client.id if client else 0),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="clcomer", placeholder="Nombre comercial", value=client.clcomer if client else "", errors=errors, autofocus=True),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="clname", placeholder="Nombre fiscal", value=client.clname if client else "", errors=errors),
            ),
        ),

        Div(cls="form-group col-md-6")(
            mk_input(id="dni_nie_cif", placeholder="DNI/NIE/CIF", value=client.dni_nie_cif if client else "", errors=errors),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="email_heading", placeholder="Email cabecera", value=client.email_heading if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="email_payment", placeholder="Email facturación", value=client.email_payment if client else "", errors=errors),
            ),
        ),

        Div(cls="form-group")(
            mk_input(id="email_payment_cc", placeholder="CC Email facturación", value=client.email_payment_cc if client else "", errors=errors),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="adress", placeholder="Dirección", value=client.adress if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-3")(
                mk_input(id="cp", placeholder="CP", value=client.cp if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-3")(
                mk_input(id="city", placeholder="Ciudad", value=client.city if client else "", errors=errors),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="state", placeholder="Provincia", value=client.state if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-3")(
                mk_input(id="country", placeholder="País", value=client.country if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-3")(
                mk_input(id="language", placeholder="Idioma", value=client.language if client else "", errors=errors),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="payment_method", placeholder="Forma de pago", value=client.payment_method if client else "", errors=errors),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="payment_responsible", placeholder="Responsable de pago", value=client.payment_responsible if client else "", errors=errors),
            ),
        ),

        Div(cls="form-group")(
            mk_input(id="notes", placeholder="Notas", value=client.notes if client else "", errors=errors),
        ),

        Div(cls="row")(
            Div(cls="d-flex justify-content-end")(
                Button(
                    cls="btn btn-secondary px-2 my-2 mx-1",
                    type="button",
                    hx_post="/clients_post",
                    hx_target="#client-modals-here",
                    hx_vals={"action2": "cancel"},
                )("Cancel"),

                Button(
                    cls="btn btn-primary px-4 my-2 mx-1",
                    type='button',
                    hx_post="/clients_post",
                    hx_target="#client-modals-here",
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

    return Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True)(
            Div(cls="boot-modal-header")(
                Div(cls="d-flex justify-content-between m-3")(
                    H3("NEW client:") if action == "add" else H4("Client: ", Span(cls="text-primary fw-bold")(f"{client.id}/{client.clcomer}")),
                    Button(cls="btn-close", type="button", hx_post="/clients_post", hx_target="#client-modals-here", hx_vals={"accion2": "cancel"}),
                ),
            ),
            Div(cls="boot-modal-body")(form)
        )
    )

def clients_navbar(session):
    return Div(
        Nav(
            cls="d-flex justify-content-start p-2 rounded gap-3",
            style="background-color: #002db3; color: white;",
            force_cls=False,
            force_style=True,
        )(
            H5("Client's Table"),
            Button(
                cls="btn btn-primary",
                hx_get="/clients_add",
                hx_trigger="click",
                hx_target="#client-modals-here",
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

def client_row(session, client: Client, client_id: int = 0):
    highlighted_cls = "highlighted" if client.id == client_id else ""
    highlighted_style = "background: rgb(255, 190, 190, 1);" if client.id == client_id else ""

    return Tr(id=f"id-{client.id}", cls=highlighted_cls)(
        Td(cls="d-flex justify-content-right btn-group-horizontal", style=highlighted_style)(
            rowButton("edit", url=f"/clients_edit/{client.id}", target="client-modals-here", icon="bi-pencil-square", color="primary"),
            rowButton("delete", url=f"/clients_delete/{client.id}", target="client-modals-here", icon="bi-trash", color="danger"),
        ),
        Td(style=highlighted_style)(f"{client.id:03}"),
        Td(style=highlighted_style)(client.clcomer),
        Td(style=highlighted_style)(client.clname),
    )

def clients_modal_confirmation(client: Client = None, action: str = "", errors: dict = {}):
    hx_vals_dict = {'action': 'delete', 'client_id': client.id if client else 0}
    return Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True, style="width: 50%;")(
            Div(cls="boot-modal-header")(
                Div(cls="m-3")(H3("Client DELETE")),
            ),
            Form()(
                Div(cls="boot-modal-body")(
                    Input(name="action", type="hidden", value=action),
                    Input(name="client_id", type="hidden", value=client.id if client else 0),
                    Div(cls="m-10")(
                        Span(cls="btn btn-danger fs-3")(errors["db"]) if "db" in errors else "",
                        H5("Are you sure you want to DELETE this client?") if "db" not in errors else "",
                        H5(f"{client.id}/{client.clcomer} - {client.clname}"),
                    ),
                ),
                Div(cls="d-flex justify-content-end boot-modal-footer")(
                    Button(
                        cls="btn btn-secondary px-2 my-2 mx-1",
                        type="button",
                        hx_post="/clients_post",
                        hx_target="#client-modals-here",
                        hx_vals={"action2": "cancel"},
                        # onclick='document.getElementById("client-modals-here").innerHTML= ""',
                    )("Cancel"),
                    Button(
                        cls="btn btn-danger px-4 my-2 mx-1",
                        type='button',
                        hx_post="/clients_post",
                        hx_target="#client-modals-here",
                        hx_vals=hx_vals_dict,
                    )("Delete") if "db" not in errors else "",
                )
            )
        )
    )

def clients_list(session, clients, client_id: int = 0):
    return Table(
        id="clients-table",
        data_page_length="10",
        cls="table table-striped table-hover display compact datatable",
        style="width: 100%; background-color: white;",
    )(
        Thead(
            Tr(
                Th(scope="col")("🛠️"),
                Th(scope="col")("ID"),
                Th(scope="col")("Código"),
                Th(scope="col")("Nombre"),
            )
        ),
        Tbody()( *[client_row(session, client, client_id=client_id) for client in clients] ),
        Tfoot(
            Tr(
                Th(scope="col", cls="dt-orderable-asc")("🛠️"),
                Th(scope="col", cls="dt-orderable-asc")("ID"),
                Th(scope="col", cls="dt-orderable-asc")("Código"),
                Th(scope="col", cls="dt-orderable-asc")("Nombre"),
            )
        ),
    )

def clients_page(session, clients, client_id: int = 0, hx_swap_oob: bool = False):
    return Div(
        clients_navbar(session),
        Div(id="client-modals-here", hx_swap_oob="true" if hx_swap_oob else "")(""),
        Div(id="clients-list", hx_swap_oob="true" if hx_swap_oob else "")(
            clients_list(session, clients, client_id=client_id)
        )
    )

