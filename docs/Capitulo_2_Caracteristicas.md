# Capítulo 2 - Características Principales (Features)

FastApp incluye múltiples funcionalidades que permiten una experiencia de usuario fluida y una arquitectura escalable:

### ✅ Gestión de Usuarios
- Ruta: `users_controller.py`
- Vista: `users_views.py`
- DAO: `DAO_users.py`

Permite realizar todas las operaciones CRUD y aplicar filtros.

### 📇 Gestión de Clientes y Contactos
- Clientes: `clients_controller.py`, `clients_views.py`
- Contactos: `contacts_controller.py`, `contacts_views.py`

Los contactos están relacionados jerárquicamente con los clientes y pueden editarse desde su propia vista o desde el modal del cliente.

### 🔐 Autenticación y Sesiones
- `auth/login.py` gestiona credenciales.
- `login_controller.py` gestiona el formulario.

### 📤 Exportación a Excel
- Implementado en `utils/excel.py`, usando `openpyxl`.
- Función `export_to_excel` permite transformar listas de diccionarios en archivos `.xlsx`.

### ⚡ Interactividad con HTMX
- Utilizado en toda la app (`hx-get`, `hx-target`, `hx-swap`).
- Mejora la experiencia cargando solo fragmentos del DOM.

### 🪟 Uso de Modales
- Formularios y acciones CRUD se presentan en ventanas modales, definidos con `fasthtml`.

### 🪜 Modales Anidados
- Ejemplo: Desde el modal de un cliente se puede abrir el de contactos sin perder contexto.

### 🔁 Rutas Modulares con `init_routes()`
- Cada archivo `controllers/*_controller.py` define una clase con un método `init_routes()`.
- Estas clases se importan desde `main.py`, facilitando la organización del código:

```python
from src.controllers.clients_controller import ClientsController

ClientsController().init_routes()
```

Esto permite una división clara del enrutamiento sin congestionar un único archivo.

### 🗃️ SQLAlchemy como ORM para la Base de Datos
FastApp utiliza la librería `SQLAlchemy` para gestionar la base de datos SQLite. Gracias a esto:

- Se puede cambiar fácilmente a otros motores como **PostgreSQL**, **MySQL** o **MariaDB** sin modificar la lógica de datos.
- El código de los modelos en `src/data/models.py` define las entidades como clases Python.
- Los DAOs (`DAO_clients.py`, `DAO_users.py`, etc.) trabajan sobre estas clases para aplicar operaciones CRUD.

Esto hace que el proyecto sea **portable, modular y escalable** en entornos productivos más exigentes.
