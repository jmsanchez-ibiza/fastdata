from dotenv import load_dotenv, find_dotenv
from fasthtml.common import *

from src.config import NAVBAR_BG_COLOR, APP_NOMBRE
from src.utils.htmx import es_hx_request
from src.views.home_views import home_page, contenido

# Cargar variables de entorno
# Busca el archivo .env
env_file = find_dotenv(".env")

if env_file and os.path.exists(env_file):
    # Carga el archivo .env si existe
    load_dotenv(env_file, override=True)
    print(f"Archivo de configuración ({env_file}) cargado exitosamente.")
else:
    # Imprime un mensaje de error y termina el programa si el archivo no se encuentra
    print("ERROR: No se encontró el fichero de configuración: .env")
    sys.exit(1)

# Leer variables de entorno
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
LIVE = os.getenv("LIVE", "False").lower() == "true"

# Bootstrap CSS (CDN)
bootstrap_css = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM",
    crossorigin="anonymous"
)

# Bootstrap JS (CDN)
bootstrap_js = Script(
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
    integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz",
    crossorigin="anonymous"
)

# Bootstrap Icons (CDN)
bootstrap_icons = Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css')()

# Activar ToolTips
bootstrap_tooltips_js = Script(
    code="""
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    """
)

scroll_to_id_js = Script(
    code='''
    function scrollToId(objId) {
        // alert("hola");
        if (!objId || objId === 'id-0') {
            // Si no hay ID, hacer scroll hasta el final de la página
            window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
        } else {
            const row = document.getElementById(objId);
            if (row) {
                row.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        }
    }
        
    // Llamar a esta función cuando se cierre el modal, pasando el ID del registro editado
    '''
)

# Definir los headers de la app
hdrs = [
    bootstrap_css,
    bootstrap_js,
    Link(rel="icon", type="image/x-ico", href="img/icon.png"),
    # Link(rel='stylesheet', href='css/mis_estilos.css', type='text/css'),
    Link(rel='stylesheet', href='css/styles.css', type='text/css'),
    Link(rel='stylesheet', href='css/modales.css', type='text/css'),
    Script(src="js/main.js"),
    Script(code="function cambiarTema(tema) {document.documentElement.setAttribute('data-theme', tema);}"),
    Script(src="https://unpkg.com/lucide@lastest"),
    Script(code=f"document.title='{APP_NOMBRE}';"),
    bootstrap_icons,
    scroll_to_id_js,
]


# JavaScript para añadir el atributo lang="es" al <html>
# script_set_lang = Script("document.documentElement.setAttribute('lang', 'es');")


# Crear la aplicación
app, rt = fast_app(
    live=LIVE,
    debug=DEBUG,
    port=PORT,
    pico=False,
    static_path="static",
    hdrs=hdrs,
    htmlkw={"lang":"es", "data-theme":"light"}, # Pasamos estos parámetros al <html>
)

# 📌 Configurar Toasts -> TENGO QUE VER COMO FUNCIONA ESTO
setup_toasts(app, duration=5)

# Estos imports van aquí abajo porque es necesario que hayamos cargado
# el archivo .env, para que esté accesible DATABASE_URL
from src.controllers import clientes_controller, usuarios_controller, obras_controller, obras_capitulos_controller, obras_pagos_previstos_controller, contratos_controller
from src.auth.login import login_required, user_role_required
from src.auth import login_routes

usuarios_controller.init_routes(rt)
clientes_controller.init_routes(rt)
obras_controller.init_routes(rt)
obras_capitulos_controller.init_routes(rt)
obras_pagos_previstos_controller.init_routes(rt)
contratos_controller.init_routes(rt)

login_routes.init_routes(rt)

# Route to serve the main page
@rt("/")
@rt("/home")
def get(session, request):

    if es_hx_request(request):
        return contenido()
    else:
        return home_page(session)


@rt('/admin')
@login_required
@user_role_required('admin')
def get(req, sess):
    user = req.scope['user']
    return Titled("Panel de Admin", P(f"Bienvenido, {user['username']}!"))


@rt('/servicios')
def get(session, request):

    ct1 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('SERVICIOS', cls='display-5 fw-normal'),
        P(cls='fs-5')(
            'This example shows how responsive offcanvas menus work within the navbar. For positioning of navbars, checkout the',
            A('top', href='/docs/5.3/examples/navbar-static/'),
            'and',
            A('fixed top', href='/docs/5.3/examples/navbar-fixed/'),
            'examples.'
        ),
        P("From the top down, you'll see a dark navbar, light navbar and a responsive navbar—each with offcanvases built in. Resize your browser window to the large breakpoint to see the toggle for the offcanvas."),
        P(
            A('Learn more about offcanvas navbars »', href='/docs/5.3/components/navbar/#offcanvas', role='button', cls='btn btn-primary')
        )
    )
    return ct1

@rt('/noticias')
def get(session, req):
    ct2 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('NOTICIAS' + f": User: {session['user_id'] if 'user_id' in session else 'No ha login'}", cls='display-5 fw-normal'),
        P(cls='fs-5')(
            'This example shows how responsive offcanvas menus work within the navbar. For positioning of navbars, checkout the',
            A('top', href='/docs/5.3/examples/navbar-static/'),
            'and',
            A('fixed top', href='/docs/5.3/examples/navbar-fixed/'),
            'examples.'
        ),
        P("From the top down, you'll see a dark navbar, light navbar and a responsive navbar—each with offcanvases built in. Resize your browser window to the large breakpoint to see the toggle for the offcanvas."),
        P(
            A('Learn more about offcanvas navbars »', href='/docs/5.3/components/navbar/#offcanvas', role='button', cls='btn btn-primary')
        )
    )
    return ct2

@rt('/contacto')
def get(session, request):

    ct3 = Div(cls='col-sm-8 py-5 mx-auto')(
        H1('CONTACTO', cls='display-5 fw-normal'),
        P(cls='fs-5')(
            'This example shows how responsive offcanvas menus work within the navbar. For positioning of navbars, checkout the',
            A('top', href='/docs/5.3/examples/navbar-static/'),
            'and',
            A('fixed top', href='/docs/5.3/examples/navbar-fixed/'),
            'examples.'
        ),
        P("From the top down, you'll see a dark navbar, light navbar and a responsive navbar—each with offcanvases built in. Resize your browser window to the large breakpoint to see the toggle for the offcanvas."),
        P(
            A('Learn more about offcanvas navbars »', href='/docs/5.3/components/navbar/#offcanvas', role='button', cls='btn btn-primary')
        )
    )

    return ct3


# Run the app
if __name__ == "__main__":
    print("EJECUTANDO CON: " + "serve()->Live" if LIVE else "Uvicorn")

    if LIVE:
        print("Serve")
        serve()
    else:
        port = int(os.getenv("PORT", default=5001))
        print(f"Uvicorn {port=} {LIVE=}")

        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=port,
            workers=4,
            reload=False
        )