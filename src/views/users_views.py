from fasthtml.common import *
from src.core.html_wrappers import *
from src.auth.login import is_user_admin
# from src.db.enums import NO_SI, SI_NO, USER_ROLE
from src.data.enums import NO_YES, USER_ROLE, YES_NO
from src.data.models import User
from src.views.components.buttons import rowButton
from src.views.components.forms import mk_input, mk_select
# from src.views.components.buttons import rowButton
# from src.views.components.forms import mk_input, mk_select


def user_form_details(user:User=None, action:str="", errors:dict={}, session={}):
    texto_boton_accion = "Add" if action=="add" else "Save"

    return \
    Form(id="user-details-form")(
        # Hidden Inputs
        Input(id="action", name="action", type="hidden", value=action),
        Input(user_id="user_id", name="user_id", type="hidden", value=user.id if user else 0),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="user_code", placeholder="User code", value="" if not user else user.user_code,
                    errors=errors, autofocus=True, autocomplete=False,
                    disabled=not is_user_admin(session),
                ),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="username", placeholder="Username", value="" if not user else user.username,
                    errors=errors, autofocus=False, autocomplete=False, capitalize=True,
                    disabled=not is_user_admin(session),
                    ),
            ),
        ),
                            
        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="name", placeholder="Name", value="" if not user else user.name, errors=errors, autofocus=False, autocomplete=False),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="email", placeholder="Email", value="" if not user else user.email, errors=errors, autofocus=False, autocomplete=False),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="password", placeholder="Password", value="" if not user else user.password, errors=errors,
                         autofocus=False, autocomplete=False,
                         disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-6")(
                mk_select(
                    id="role",
                    placeholder="Role",
                    data_value="" if not user else user.role,
                    data_dict=USER_ROLE,
                    errors=errors,
                    autofocus=True,
                    autocomplete=False,
                    disabled=not is_user_admin(session)),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-4")(
                mk_select(
                    id="active",
                    placeholder="Active?",
                    data_value="" if not user else user.active,
                    data_dict=YES_NO,
                    errors=errors,
                    autofocus=True,
                    autocomplete=False,
                    disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-4")(
                mk_select(
                    id="blocked",
                    placeholder="Blocked?",
                    data_value="" if not user else user.blocked,
                    data_dict=NO_YES,
                    errors=errors,
                    autofocus=True,
                    autocomplete=False,
                    disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-4")(
                mk_input(id="last_login", placeholder="Last login", value="" if not user else user.last_login, errors=errors, autofocus=False, autocomplete=False, disabled=True),
            ),
        ),

        # Footer
        Div(cls="row")(
            Div(cls="d-flex justify-content-end")(
                Button(
                    cls="btn btn-secondary px-2 my-2 mx-1",
                    type="button",
                    hx_post="/users_post",
                    hx_target="#user-modals-here",
                    hx_vals={"action2": "cancel"},
                    # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')"
                )("Cancel"),

                Button(
                    cls="btn btn-primary px-4 my-2 mx-1",
                    type='button',
                    hx_post="/users_post",
                    hx_target="#user-modals-here",
                    hx_indicator="#spinner",
                )(
                    Div(cls="d-flex align-items-center gap-2")(
                        f"{texto_boton_accion.capitalize()}",
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
    ) # Fin Form

def users_form(session={}, action:str="edit", user:User=None, errors:dict={}):
    
    if action=="add":
        #  If there's no error, it's a new (empty) record  
        #  If there's an error, the form needs to be filled out again
        user = User() if not errors else user

    form = \
    Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True)(

            # Header
            Div(cls="boot-modal-header")(
                Div(cls="d-flex justify-content-between m-3")(
                    H3("NEW user:")
                        if action=="add" 
                        else
                        H4(
                            "User: ",
                            Span(cls="text-primary fw-bold")(f"{user.id}/{user.user_code}- {user.username.strip()}")
                        ),
                    Button(cls="btn-close", type="button", hx_post="/users_post", hx_target="#user-modals-here", hx_vals={"accion2": "cancel"}),
                ),
            ),

            # Body
            Div(cls="boot-modal-body")(
                Div(cls="nav")(
                    Span(cls="card mb-2 p-2 bg-warning text-black")(errors['db'])
                ) if "db" in errors else "",
                
                Ul(id='user-tab', role='tablist', cls='nav nav-pills mb-3')(
                    Li(role='presentation', cls='nav-item')(
                        Button(id='user-details-tab', data_bs_toggle='pill', data_bs_target='#users-details', type='button', role='tab', aria_controls='users-details', aria_selected='true', cls='nav-link active')('User details')
                    ),
                    Li(role='presentation', cls='nav-item')(
                        Button(id='base-tab2', data_bs_toggle='pill', data_bs_target='#data-tab2', type='button', role='tab', aria_controls='data-tab2', aria_selected='false', cls='nav-link')('DataTab-2')
                    ),
                ),

                Div(id='users-tabContent', cls='tab-content')(
                    Div(id='users-details', role='tabpanel', aria_labelledby='user-details-tab', cls='tab-pane fade show active')(
                        user_form_details(user=user, action=action, errors=errors, session=session)
                    ),
                    Div(id='data-tab2', role='tabpanel', aria_labelledby='base-tab2', cls='tab-pane fade')(
                        Span(cls="btn btn-danger")("PAGE UNDER CONSTRUCTION (users)"),
                    ),
                ),
            ),
        )
    )

    return form

def users_navbar(session):
    return \
    Div(
        Nav(
            cls="d-flex justify-content-start p-2 rounded gap-3",
            style="background-color: #002db3; color: white;",
            force_cls=False,
            force_style=True,
        )(
            H5("User's Table"),
            Button(
                cls="btn btn-primary",
                hx_get="/users_add",
                hx_trigger="click",
                hx_target="#user-modals-here",

            )(
                I(cls="bi-plus-circle text-white fs-5"),
                Span(cls="mx-1")("Add"),
            ),

            Button(cls="btn btn-primary disabled")(
                (
                    I(cls="bi-printer text-white fs-5"),
                    Span(cls="mx-1")("Reports"),
                )
            ),
            Button(cls="btn btn-primary disabled")(
                (
                    I(cls="bi-folder-symlink text-white fs-5"),
                    Span(cls="mx-1")("Export"),
                )
            ),
            
        )
    )

def user_row(session, user:User, user_id:int=0):
    # If a user has been specified, assign the classes and styles to highlight that row
    highlighted_cls = "highlighted" if user.id == user_id else ""
    highlighted_style = "background: rgb(255, 190, 190, 1);" if user.id == user_id else ""
    
    return Tr(id=f"id-{user.id}", cls=highlighted_cls)(
        Td(cls="d-flex justify-content-right btn-group-horizontal", style=highlighted_style)(
            rowButton(accion="edit", url=f"/users_edit/{user.id}", target="user-modals-here", icon="bi-pencil-square", color="primary"),
            rowButton(accion="delete", url=f"/users_delete/{user.id}", target="user-modals-here", icon="bi-trash", color="danger",
                      disabled=True if user and user.role=="admin" else False),
        ),
        Td(style=highlighted_style)(f"{user.id}/{user.user_code:03}"),
        Td(cls="fw-bold", style=highlighted_style)(user.username.strip()),
        Td(style=highlighted_style)(user.name),
        Td(style=highlighted_style)(user.role),
    )

def users_modal_confirmation(user:User=None, action:str="", errors:dict={}):

    hx_vals_dict = {'action': 'delete', 'user_id': user.id if user else 0}
    form = \
    Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True, style="width: 50%;")(

            # Header
            Div(cls="boot-modal-header")(
                Div(cls="m-3")(
                    H3("User DELETE"),
                ),
            ),

            Form()(

                # Body
                Div(cls="boot-modal-body")(
                    Input(id="action", name="action", type="hidden", value=action),
                    Input(id="user_id", name="user_id", type="hidden", value=user.id if user else 0),

                    Div(cls="m-10")(
                        Span(cls="btn btn-danger fs-3")(errors["db"]) if "db" in errors else "",
                        H5("Are you sure you want to DELETE this user?") if not "db" in errors else "",
                        H5(f"{user.id}/{user.user_code} - {user.username}"),
                    ),

                ),

                # Footer
                Div(cls="d-flex justify-content-end boot-modal-footer")(
                    Button(
                        cls="btn btn-secondary px-2 my-2 mx-1",
                        type="button",
                        hx_post="/users_post",
                        hx_target="#user-modals-here",
                        hx_vals={"action2": "cancel"},
                        # onclick='document.getElementById("user-modals-here").innerHTML= ""',
                    )("Cancel"),

                    Button(
                        cls=f"btn btn-{'danger' if action=='delete' else 'primary'} px-4 my-2 mx-1",
                        type='button',
                        hx_post="/users_post",
                        hx_target="#user-modals-here",
                        hx_vals=hx_vals_dict,
                        # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')",
                    )("Add" if action=="add" else "Save" if action=="edit" else "Delete") if not "db" in errors else "",
                ),

            ), # Fin Form
        )
    )

    return form

def users_list(session, users, user_id:int=0, hx_swap_oob:bool=False):

    clients_table = Table(
        id="users-table",
        data_page_length="10",
        cls="table table-striped table-hover display compact datatable",  # datatable, es la clase necesaria para transformarla en DataTable
        style="width: 100%; background-color: white;",
        # hx_swap_oob="true" if hx_swap_oob else "",
        )(
        Thead(
            Tr(
                Th(scope="col")("🛠️"),
                Th(scope="col")("Id/Code"),
                Th(scope="col")("Username"),
                Th(scope="col")("Name"),
                Th(scope="col")("Role"),
            )
        ),
        Tbody()(
            *[user_row(session, user, user_id = user_id) for user in users]
        ),
        Tfoot(
            Tr(
                Th(scope="col", cls="dt-orderable-asc")("🛠️"),
                Th(scope="col", cls="dt-orderable-asc")("Id/Code"),
                Th(scope="col", cls="dt-orderable-asc")("Username"),
                Th(scope="col", cls="dt-orderable-asc")("Name"),
                Th(scope="col", cls="dt-orderable-asc")("Role"),
            )
        ),
    )

    return clients_table

def users_page(session, users, user_id:int=0, hx_swap_oob:bool=False):
    return \
    Div(
        users_navbar(session),
        Div(id="user-modals-here", hx_swap_oob="true" if hx_swap_oob else "")(""),
        Div(id="users-list", hx_swap_oob="true" if hx_swap_oob else "")(
            users_list(session, users, user_id=user_id),
        )
    )

