# Capítulo 6 - Flujo de Ejecución

El flujo de ejecución en FastApp sigue una estructura lógica basada en el patrón MVC (Modelo-Vista-Controlador), con integración de rutas a través de clases y renderizado HTML mediante `fasthtml`. A continuación se describe paso a paso lo que ocurre desde que se inicia la aplicación hasta que se responde a una petición del usuario.

---

## 🚀 1. Inicio de la Aplicación

La aplicación comienza su ejecución en el archivo `main.py`.


### ¿Qué ocurre aquí?

- Se importa la instancia de `app` de `fasthtml`, y se inicia la aplicación `app`
- Se inicializan las rutas desde los controladores con `init_routes(rt)`.
- Se arranca el servidor local con `serve` o con `uvicorn`.
- Para producción recomiento el uso de `uvicorn` tal como aparece en `main.py`

---

## 🌐 2. Petición HTTP del Cliente

Cuando un usuario accede a la aplicación desde un navegador (por ejemplo, `http://localhost:5001/users`), se dispara una petición GET al servidor.

---

## 🧭 3. Enrutamiento mediante la función init_routes() de las clases `Controllers`

Cada controlador define las rutas usando las clases `Controllers`, en lugar de usar el decorador `@rt()`
Para poder dividir el código en distintos archivos, en lugar de concentrarlo todo en el `main.py`

Ejemplo de `users_controller.py`:
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


...

```

- `rt` es el contexto para el enrutamiento proveniente de la `app`
- Se consulta la base de datos a través de un DAO.
- Se retorna una vista HTML construida con `fasthtml`.

---

## 🛠️ 4. Lógica del Controlador

Cada controlador contiene funciones que definen:
- Qué ruta manejar.
- Qué datos obtener o modificar.
- Qué vista retornar.
- Cómo validar la entrada del usuario.

---

## 🧩 5. Renderizado HTML con fasthtml

El renderizado del código HTML se hace con **fasthtml** y sus fast-tags (ft), usados como funciones
que retorna el código HTML necesario.

Ejemplo:
```python
def home_page(session, request):
    return Div(cls="container")(
        H1("Página principal"),
        P("Texto de un párrafo"),
        Ul()(
            Li(cls="text-danger nav-link")("Opción 1"),
            Li(cls="text-danger nav-link")("Opción 2"),
            Li(cls="text-danger nav-link")("Opción 3"),
        )
    )

    ...
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

Con las funciones y decoradores definidos en src/auth/login.py, como:
- login_required()
- user_role_required()
- is_user_logged()
- get_user_info()
- is_user_admin()

Se puede personalizar el acceso a diferentes partes de la aplicación, según si se ha
loggeado un usuario en el sistema, o según el role del usuario loggeado.

Este sistema se basa en el uso de `session` como diccionario de almacenamiento accesible
desde las rutas de la aplicación.


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
2. Se ejecuta `form_edit()` en `users_controller.py`.
3. Se genera el modal en `users_views.users_form()`.
4. El HTML parcial se inyecta en el modal (`#user-modals-here`).
5. Usuario edita datos y envía el formulario → `hx-post="/users_post"`.
6. Se ejecuta `process_post` y se actualiza la base de datos.
7. Se recarga la tabla de usuarios con HTMX.

---

Este flujo claro y organizado facilita el mantenimiento, la depuración y la escalabilidad del proyecto.
