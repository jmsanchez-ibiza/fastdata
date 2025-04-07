from dotenv import load_dotenv, find_dotenv
from fasthtml.common import *

from src.config import APP_NAME
from src.utils.js_scripts import scroll_to_id_js

# Load environment variables  
# Look for the .env file
env_file = find_dotenv(".env")

if env_file and os.path.exists(env_file):
    # Load the .env file if it exists
    load_dotenv(env_file, override=True)
    print(f"Configuration file ({env_file}) successfully loaded.")
else:
    # Print an error message and terminate the program if the file is not found.
    print("ERROR: Configuration file not found: .env")
    sys.exit(1)

# Read environment variables.
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

# JQuery JS (CDN)
jquery_js = Script(src='https://code.jquery.com/jquery-3.7.1.js')

# Datatables.net, I have disabled those that are not necessary for the project.
# datatables_jquery_css = Link(rel='stylesheet', type='text/css', href='https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css')
# datatables_css = Link(rel='stylesheet', type='text/css', href='https://cdn.datatables.net//css/jquery.dataTables.min.css')
# datatables_css = Link(rel='stylesheet', type='text/css', href='https://cdn.datatables.net/2.2.2/css/dataTables.dataTables.css')
# datatables_js = Script(type='text/javascript', charset='utf8', src='https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js')
datatables_css_bs = Link(rel='stylesheet', type='text/css', href='https://cdn.datatables.net/2.2.2/css/dataTables.bootstrap5.min.css')
datatables_js = Script(type='text/javascript', charset='utf8', src='https://cdn.datatables.net/2.2.2/js/dataTables.js')
datatables_js_bs = Script(type='text/javascript', charset='utf8', src='https://cdn.datatables.net/2.2.2/js/dataTables.bootstrap5.js')

# Scripts to incorporate buttons into DataTables, now disabled as they're not needed.
# datatables_jzcip = Script(src='https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js')
# datatables_datatables_buttons = Script(src='https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js')
# datatables_buttons_bs = Script(src='https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js')
# datatables_buttons = Script(src='https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js')

# Set the app headers.
hdrs = [
    bootstrap_css,
    bootstrap_js,
    jquery_js,
    # datatables_jquery_css,
    # datatables_css,
    datatables_css_bs,
    datatables_js,
    datatables_js_bs,
    # datatables_jzcip,
    # datatables_datatables_buttons,
    # datatables_buttons_bs,
    # datatables_buttons,
    Link(rel="icon", type="image/x-ico", href="img/recycle.png"),
    Link(rel='stylesheet', href='css/styles.css', type='text/css'),
    Link(rel='stylesheet', href='css/modals.css', type='text/css'),
    Script(src="js/main.js"),
    Script(code="function cambiarTema(tema) {document.documentElement.setAttribute('data-theme', tema);}"),
    Script(src="https://unpkg.com/lucide@lastest"),
    Script(code=f"document.title='{APP_NAME}';"), # Change browser window title
    bootstrap_icons,
    scroll_to_id_js,
]


# JavaScript To add the attribute lang="es" to the <html> tag.
# script_set_lang = Script("document.documentElement.setAttribute('lang', 'es');")


# Create the application.
app, rt = fast_app(
    live=LIVE,
    debug=DEBUG,
    port=PORT,
    pico=False,
    static_path="static",
    hdrs=hdrs,
    htmlkw={"lang":"es", "data-theme":"light"}, # Pasamos estos parámetros al <html>, lang: "es" for Spanish, "en" for English.
)

# Add Toasts to app
setup_toasts(app, duration=3000)

# These imports go here below because it's necessary to have loaded  
# the .env file first, so DATABASE_URL is accessible
from src.controllers import (
    home_controller, login_controller, users_controller, 
    clients_controller, contacts_controller
)

# Import all controller routes.
home_controller.init_routes(rt)
login_controller.init_routes(rt)
users_controller.init_routes(rt)
clients_controller.init_routes(rt)
contacts_controller.init_routes(rt)

# Run the app
if __name__ == "__main__":
    print("RUNNING WITH: " + "serve()->Live" if LIVE else "Uvicorn")

    if LIVE:
        print("Serve")
        serve()
    else:
        port = int(os.getenv("PORT", default=5001))
        print(f"Uvicorn {port=} {LIVE=}")

        # Using uvicontn to run the app with 4 workers.
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=port,
            workers=4,
            reload=False
        )