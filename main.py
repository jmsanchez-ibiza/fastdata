from dotenv import load_dotenv, find_dotenv
from fasthtml.common import *

from src.config import APP_NAME
from src.utils.js_scripts import scroll_to_id_js

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


# Definir los headers de la app
hdrs = [
    bootstrap_css,
    bootstrap_js,
    Link(rel="icon", type="image/x-ico", href="img/recycle.png"),
    Link(rel='stylesheet', href='css/styles.css', type='text/css'),
    Link(rel='stylesheet', href='css/modales.css', type='text/css'),
    Script(src="js/main.js"),
    Script(code="function cambiarTema(tema) {document.documentElement.setAttribute('data-theme', tema);}"),
    Script(src="https://unpkg.com/lucide@lastest"),
    Script(code=f"document.title='{APP_NAME}';"), # Change browser window title
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

# 📌 Add Toasts to app
# setup_toasts(app, duration=5000)

# Estos imports van aquí abajo porque es necesario que hayamos cargado
# el archivo .env, para que esté accesible DATABASE_URL
from src.controllers import home_controller, login_controller
# from src.auth.login import login_required, user_role_required
# from src.auth import login_routes

home_controller.init_routes(rt)
login_controller.init_routes(rt)

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