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

'''
def row_usuario(usuario:User, user_id:int=0):
    highlighted_cls = "animado" if usuario.id == user_id else ""
    marcado_style = "background: rgb(255, 190, 190, 1);" if usuario.id == user_id else ""
    return Tr(id=f"id-{usuario.id}", cls=animado_cls)(
        Td(cls="d-flex justify-content-right btn-group-horizontal", style=marcado_style)(
            rowButton(accion="editar", url=f"/usuario_editar/{usuario.id}", target="usuario-modals-here", icon="bi-pencil-square", color="primary"),
            rowButton("borrar", url=f"/usuario_borrar/{usuario.id}", target="usuario-modals-here", icon="bi-trash", color="danger"),
        ),
        Td(style=marcado_style)(f"{usuario.id}/{usuario.user_code:03}"),
        Td(cls="fw-bold", style=marcado_style)(usuario.username.strip()),
        Td(style=marcado_style)(usuario.nombre_completo),
    )

def lista_usuarios(usuarios, user_id:int=0):
    return Table(cls="table table-responsive table-striped table-hover")(  #  table-stripped table-focus
        Thead(
            Tr(
                Th(scope="col")("🛠️"),
                Th(scope="col")("Id/Cód"),
                Th(scope="col")("Username"),
                Th(scope="col")("Nombre"),
            ),
        ),

        Tbody(cls="table-group-divider")(
            *[row_usuario(x, user_id=user_id) for x in usuarios]
        ),
    )

def form_usuarios_campos_base(usuario:User=None, accion:str="", errors:dict={}, session={}):
    texto_boton_accion = "Añadir" if accion=="crear" else "Guardar" if accion=="editar" else "Borrar"

    return \
    Form(id="form-usuario-base")(
        # Campos Hidden
        Input(id="accion", name="accion", type="hidden", value=accion),
        Input(id="id", name="id", type="hidden", value=usuario.id if usuario else 0),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="user_code", placeholder="Código usuario", value="" if not usuario else usuario.user_code,
                    errors=errors, autofocus=True, autocomplete=False,
                    disabled=not is_user_admin(session),
                ),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="username", placeholder="Username", value="" if not usuario else usuario.username,
                    errors=errors, autofocus=False, autocomplete=False,
                    disabled=not is_user_admin(session),
                    ),
            ),
        ),
                            
        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="nombre_completo", placeholder="Nombre completo", value="" if not usuario else usuario.nombre_completo, errors=errors, autofocus=False, autocomplete=False),
            ),
            Div(cls="form-group col-md-6")(
                mk_input(id="email", placeholder="Email", value="" if not usuario else usuario.email, errors=errors, autofocus=False, autocomplete=False),
            ),
        ),

        Div(cls="row")(
            Div(cls="form-group col-md-6")(
                mk_input(id="password", placeholder="Password", value="" if not usuario else usuario.password, errors=errors,
                         autofocus=False, autocomplete=False,
                         disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-6")(
                mk_select(
                    id="role",
                    placeholder="Grupo",
                    data_value="" if not usuario else usuario.role,
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
                    id="activo",
                    placeholder="Activo?",
                    data_value="" if not usuario else usuario.activo,
                    data_dict=SI_NO,
                    errors=errors,
                    autofocus=True,
                    autocomplete=False,
                    disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-4")(
                mk_select(
                    id="bloqueado",
                    placeholder="Bloqueado?",
                    data_value="" if not usuario else usuario.bloqueado,
                    data_dict=NO_SI,
                    errors=errors,
                    autofocus=True,
                    autocomplete=False,
                    disabled=not is_user_admin(session)),
            ),
            Div(cls="form-group col-md-4")(
                mk_input(id="last_login", placeholder="Último login", value="" if not usuario else usuario.last_login, errors=errors, autofocus=False, autocomplete=False, disabled=True),
            ),
        ),

        # Footer
        Div(cls="row")(
            Div(cls="d-flex justify-content-end")(
                Button(
                    cls="btn btn-secondary px-2 my-2 mx-1",
                    type="button",
                    hx_post="/usuario_post",
                    hx_target="#usuario-modals-here",
                    hx_vals={"accion2": "cancelar"},
                    # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')"
                )("Cancelar"),

                Button(
                    cls="btn btn-primary px-4 my-2 mx-1",
                    type='button',
                    hx_post="/usuario_post",
                    hx_target="#usuario-modals-here",
                    # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')",
                )(f"{texto_boton_accion.capitalize()}"),
            ),
        ),
    ) # Fin Form

def form_usuarios(usuario:User=None, accion:str="editar", errors:dict={}, session={}):
    
    if accion=="crear":
        #  Si no hay error, es un registro nuevo (vacío)
        #  Si hay error, es necesario volver a llenar el form con cliente
        usuario = User() if not errors else usuario
        # TODO: falta por implementar -> usuario.asignar_defaults()

    form_usuarios = \
    Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True)(

            # Header
            Div(cls="boot-modal-header")(
                Div(cls="d-flex justify-content-between m-3")(
                    H3("NUEVO Usuario:")
                        if accion=="crear" 
                        else
                        H4(
                            "Usuario: ",
                            Span(cls="text-primary fw-bold")(f"{usuario.id}/{usuario.user_code}- {usuario.username.strip()}")
                        ),
                    Button(cls="btn-close", type="button", hx_post="/usuario_post", hx_target="#usuario-modals-here", hx_vals={"accion2": "cancelar"}),
                ),
            ),

            # Body
            Div(cls="boot-modal-body")(
                Div(cls="nav")(
                    Span(cls="card mb-2 p-2 bg-warning text-black")(errors['db'])
                ) if "db" in errors else "",
                
                Ul(id='usuarios-tab', role='tablist', cls='nav nav-pills mb-3')(
                    Li(role='presentation', cls='nav-item')(
                        Button(id='usuarios-base-tab', data_bs_toggle='pill', data_bs_target='#usuarios-base', type='button', role='tab', aria_controls='usuarios-base', aria_selected='true', cls='nav-link active')('Datos')
                    ),
                    Li(role='presentation', cls='nav-item')(
                        Button(id='base-tab2', data_bs_toggle='pill', data_bs_target='#data-tab2', type='button', role='tab', aria_controls='data-tab2', aria_selected='false', cls='nav-link')('Tab-2')
                    ) if accion=="editar" else "",
                ),

                Div(id='usuarios-tabContent', cls='tab-content')(
                    Div(id='usuarios-base', role='tabpanel', aria_labelledby='usuarios-base-tab', cls='tab-pane fade show active')(
                        form_usuarios_campos_base(usuario=usuario, accion=accion, errors=errors, session=session),
                    ),
                    Div(id='data-tab2', role='tabpanel', aria_labelledby='base-tab2', cls='tab-pane fade')(
                        Span(cls="btn btn-danger")("EN CONSTRUCCIÓN (usuarios)"),
                    ),
                ),
            ),
        )
    )


    return form_usuarios

def form_usuarios_confirmacion(usuario:User=None, accion:str="", errors:dict={}):

    form_confirmacion = \
    Div(cls="boot-modal")(
        Dialog(cls='container boot-modal-content', _open=True, style="width: 50%;")(

            # Header
            Div(cls="boot-modal-header")(
                Div(cls="m-3")(
                    H3("Acción: BORRAR usuario"),
                ),
            ),

            Form()(

                # Body
                Div(cls="boot-modal-body")(
                    Input(id="accion", name="accion", type="hidden", value=accion),
                    Input(id="id", name="id", type="hidden", value=usuario.id if usuario else 0),

                    Div(cls="m-10")(
                        Span(cls="btn btn-danger fs-3")(errors["db"]) if "db" in errors else "",
                        H5("¿Está seguro de BORRAR este usuario?") if not "db" in errors else "",
                        H5(f"{usuario.id}/{usuario.user_code} - {usuario.username}"),
                    ),

                ),

                # Footer
                Div(cls="d-flex justify-content-end boot-modal-footer")(
                    Button(
                        cls="btn btn-secondary px-2 my-2 mx-1",
                        type="button",
                        onclick='document.getElementById("usuario-modals-here").innerHTML= ""',
                    )("Cancelar"),

                    Button(
                        cls=f"btn btn-{'danger' if accion=='borrar' else 'primary'} px-4 my-2 mx-1",
                        type='button',
                        hx_post="/usuario_post",
                        hx_target="#usuario-modals-here",
                        hx_vals='{"accion": "borrar", "cliente_id": "'+str(usuario.id)+'"}',
                        # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')",
                    )("Añadir" if accion=="crear" else "Guardar" if accion=="editar" else "Borrar") if not "db" in errors else "",
                ),

            ), # Fin Form
        )
    )

    return form_confirmacion
'''

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
                    # onclick=f"scrollToId('id-{usuario.id if usuario and usuario.id else 0}')",
                )(f"{texto_boton_accion.capitalize()}"),
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
                        onclick='document.getElementById("user-modals-here").innerHTML= ""',
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
                Th(scope="col")("🛠️"),
                Th(scope="col")("Id/Code"),
                Th(scope="col")("Username"),
                Th(scope="col")("Name"),
                Th(scope="col")("Role"),
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

