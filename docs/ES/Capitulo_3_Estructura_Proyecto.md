# Capítulo 3 - Estructura del Proyecto

La estructura del proyecto FastApp está organizada para seguir el patrón **MVC** (Modelo - Vista - Controlador), lo cual permite separar claramente la lógica de negocio, la presentación y el acceso a datos.

A continuación, se describe el contenido y propósito de cada carpeta:

```
fastapp/
├── main.py
├── .env
├── fastdata.db
├── src/
│   ├── auth/
│   ├── controllers/
│   ├── core/
│   ├── data/
│   ├── utils/
│   └── views/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
```

### `main.py`
Archivo principal que inicializa la aplicación. Importa los controladores y llama a sus métodos `init_routes()` para registrar las rutas.

```python
from src.controllers.clients_controller import ClientsController
ClientsController().init_routes(rt)
```

### `src/auth/`
Contiene lógica de autenticación como la verificación de credenciales (`login.py`).

### `src/controllers/`
Define las rutas de la aplicación y su lógica de control. Cada controlador gestiona una entidad específica.

Ejemplo:
```python
class UsersController:

    def __init__(self, rt):
        self.rt = rt
        self.init_routes()

    def init_routes(self):
        self.rt("/users")(login_required(self.list))
        self.rt("/users_add")(login_required(self.form_add))
        self.rt("/users_edit/{user_id}")(login_required(self.form_edit))
        self.rt("/users_delete/{user_id}")(login_required(self.form_delete))
        self.rt("/users_post")(self.process_post)

    def list(self, session, request):
        try:
            users = UserDAO().get_all(order_by={"username": "ASC"})
            return users_page(session, users)
        except Exception as e:
            return error_msg(f"ERROR: {e}")
    ...
```

### `src/core/`
Funciones que encapsulan lógica común, como envoltorios HTML (`html_wrappers.py`) compatibles con fasthtml.
Esta utilidad permite personalizar el diseño de los fast-tags (ft) para cada aplicación.

### `src/data/`
Contiene los modelos de datos y DAOs. También se encuentra aquí la configuración de SQLAlchemy y las utilidades de validación.

- `models.py`: Clases base de modelos con SQLAlchemy
- `validators.py`: Utilidades para usar en validación de datos.
- `database.py`: Conexión con la base de datos (en este ejemplo con SQLite)

### `src/views/`
Las vistas son construidas con `fasthtml`. Cada archivo define funciones que generan HTML estructurado con Python.

Ejemplo:
```python
def users_page(session, users, user_id:int=0, hx_swap_oob:bool=False):
    return \
    Div(
        users_navbar(session),
        Div(id="user-modals-here", hx_swap_oob="true" if hx_swap_oob else "")(""),
        Div(id="users-list", hx_swap_oob="true" if hx_swap_oob else "")(
            users_list(session, users, user_id=user_id),
        )
    )

    ...
```

### `src/utils/`
Funciones auxiliares como exportación a Excel (`excel.py`), scripts JavaScript, integración con HTMX.

### `static/`
Contiene recursos estáticos accesibles desde el navegador:
- CSS personalizados
- JavaScript para interactividad
- Íconos y animaciones

Esta estructura modular permite mantener el proyecto ordenado, testable y fácil de ampliar.
