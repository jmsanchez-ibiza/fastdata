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
ClientsController().init_routes()
```

### `src/auth/`
Contiene lógica de autenticación como la verificación de credenciales (`login.py`).

### `src/controllers/`
Define las rutas de la aplicación y su lógica de control. Cada controlador gestiona una entidad específica.

Ejemplo:
```python
@route("/users")
def index(ctx):
    ...
```

### `src/core/`
Funciones que encapsulan lógica común, como envoltorios HTML (`html_wrappers.py`) compatibles con fasthtml.

### `src/data/`
Contiene los modelos de datos y DAOs. También se encuentra aquí la configuración de SQLAlchemy y las utilidades de validación.

- `models.py`: Clases base con SQLAlchemy
- `validators.py`: Validación de entradas del usuario
- `database.py`: Conexión con SQLite

### `src/views/`
Las vistas son construidas con `fasthtml`. Cada archivo define funciones que generan HTML estructurado con Python.

Ejemplo:
```python
def user_table(users):
    with Table():
        for user in users:
            Tr(Td(user.name), Td(user.email))
```

### `src/utils/`
Funciones auxiliares como exportación a Excel (`excel.py`), scripts JavaScript, integración con HTMX.

### `static/`
Contiene recursos estáticos accesibles desde el navegador:
- CSS personalizados
- JavaScript para interactividad
- Íconos y animaciones

Esta estructura modular permite mantener el proyecto ordenado, testable y fácil de ampliar.
