from fasthtml.common import *
from src.core.html_wrappers import *

def login_form(errors: str = ""):
    return \
    Div(cls="row justify-content-center")(
        Div(cls="col-md-6 p-6")(
            Form(action="/login_post", method="POST", cls="boot-modal-content p-6")(
                Div(cls="boot-modal-header text-center")(
                    H3(cls="text-primary fs-3")("fastDATA Login"),
                ),
                Div(cls="boot-modal-body")(
                    Div(cls="form-group")(
                        
                        Div(cls='form-floating')(
                            Input(
                                type="input",
                                id="f-username",
                                name="username",
                                placeholder='Username',
                                cls='form-control my-4',
                                autofocus=True, autocomplete="on",
                            ),
                            Label('Username', fr='f-username'),
                        ),
                        
                        Div(cls='form-floating')(
                            Input(
                                type='password',
                                id='f-password',
                                name="password",
                                placeholder='Password',
                                cls='form-control my-4'
                            ),
                            Label('Password', fr='f-password'),
                        ),
                        Input(type="hidden", name="user_role", value="user"),  
                    )
                ),
                Div(cls="boot-modal-footer text-center")(
                    Button(cls="btn btn-secondary my-2 mx-2", type="button", hx_get="/", hx_target="#main-content", hx_swap="innerHTML")("Cancel"),
                    Button(cls="btn btn-primary my-2", type="submit")("Login"),
                )
            ) # End of Form
        )
    )