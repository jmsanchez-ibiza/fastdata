# Capítulo 6 - Flujo de Ejecución

El flujo de ejecución en FastApp sigue una estructura lógica basada en el patrón MVC (Modelo-Vista-Controlador), con integración de rutas a través de clases y renderizado HTML mediante `fasthtml`. A continuación se describe paso a paso lo que ocurre desde que se inicia la aplicación hasta que se responde a una petición del usuario.

---

## 🚀 1. Inicio de la Aplicación

La aplicación comienza su ejecución en el archivo `main.py`.

```python
from fasthtml import app
from src.controllers.clients_controller import ClientsController
from src.controllers.users_controller import UsersController

ClientsController().init_routes()
UsersController().init_routes()

app.run()
```

### ¿Qué ocurre aquí?

- Se importa la instancia de `app` de `fasthtml`.
- Se inicializan las rutas desde los controladores con `init_routes()`.
- Se arranca el servidor local con `app.run()`.

---

## 🌐 2. Petición HTTP del Cliente

Cuando un usuario accede a la aplicación desde un navegador (por ejemplo, `http://localhost:8000/users`), se dispara una petición GET al servidor.

---

## 🧭 3. Enrutamiento con `@route()`

Cada controlador define las rutas usando decoradores `@route()` de `fasthtml`.

Ejemplo de `users_controller.py`:
```python
@route("/users")
def index(ctx):
    users = DAOUsers().get_all()
    return UsersViews.index(users)
```

- `ctx` es el contexto de la petición.
- Se consulta la base de datos a través de un DAO.
- Se retorna una vista HTML construida con `fasthtml`.

---

## 🛠️ 4. Lógica del Controlador

Cada controlador contiene funciones que definen:
- Qué ruta manejar.
- Qué datos obtener o modificar.
- Qué vista retornar.
- Cómo validar la entrada del usuario.

En el ejemplo anterior:
- Se obtiene una lista de usuarios.
- Se llama a `UsersViews.index(users)` para generar la vista.

---

## 🧩 5. Renderizado HTML con fasthtml

En `users_views.py`, se define una función que genera el HTML completo dinámicamente:

```python
def index(users):
    with Div():
        H1("Lista de Usuarios")
        with Table(_class="table datatable"):
            for user in users:
                Tr(Td(user.name), Td(user.email))
```

Este código:
- Utiliza bloques anidados.
- Aplica clases CSS.
- Construye componentes reutilizables.

---

## 🔁 6. Respuesta al Cliente

El resultado es HTML puro que se envía al navegador, donde se renderiza directamente.

Si la petición se originó desde HTMX (por ejemplo, al hacer clic en un botón de edición), solo una parte del DOM se actualiza gracias a atributos como `hx-target` y `hx-swap`.

---

## 🔒 7. Verificación de Autenticación

Muchas rutas están protegidas con el decorador `@authenticated`, por ejemplo:

```python
@route("/users")
@authenticated
def index(ctx):
    ...
```

Este decorador comprueba si el usuario tiene una sesión activa y, en caso contrario, lo redirige a la página de login.

---

## 🔄 8. Interactividad

Cuando se realizan acciones como:
- Enviar un formulario
- Abrir un modal
- Editar una tabla

Todo ocurre mediante llamadas a rutas controladas, y se actualizan vistas parciales gracias a HTMX. No se usan páginas completas, sino fragmentos del DOM.

---

## ✅ Ejemplo de flujo completo (editar un usuario)

1. Usuario hace clic en "Editar" → Se dispara `hx-get="/users/edit/5"`.
2. Se ejecuta `edit(ctx)` en `users_controller.py`.
3. Se genera el modal en `users_views.edit(user)`.
4. El HTML parcial se inyecta en el modal (`#modal-body`).
5. Usuario edita datos y envía el formulario → `hx-post="/users/update"`.
6. Se ejecuta `update(ctx)` y se actualiza la base de datos.
7. Se recarga la tabla de usuarios con HTMX.

---

Este flujo claro y organizado facilita el mantenimiento, la depuración y la escalabilidad del proyecto.
