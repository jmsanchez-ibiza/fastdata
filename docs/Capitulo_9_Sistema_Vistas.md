# Capítulo 9 - Sistema de Vistas

El sistema de vistas en FastApp está construido íntegramente con la librería `fasthtml`, que permite generar interfaces HTML dinámicas y estructuradas directamente desde código Python. Esta aproximación elimina la necesidad de plantillas HTML tradicionales, lo que favorece una mayor cohesión del código y facilita la reutilización de componentes.

---

## 🧩 ¿Qué es fasthtml?

`fasthtml` es una librería que transforma estructuras Python en árboles DOM HTML de forma declarativa. Usa una sintaxis de bloques anidados y atributos similares a los del HTML.

---

## 🏗️ Organización de Vistas

Las vistas se encuentran en `src/views/` y están organizadas por entidad:

- `users_views.py`
- `clients_views.py`
- `contacts_views.py`
- `home_views.py`
- `login_views.py`
- `components/`: botones y formularios reutilizables
- `utils.py`: funciones de renderizado comunes

---

## 🧱 Ejemplo de Vista Básica

Archivo: `users_views.py`

```python
def index(users):
    with Div():
        H1("Lista de Usuarios")
        with Table(_class="table datatable"):
            for user in users:
                Tr(Td(user.name), Td(user.email), Td(buttons.edit_button(user.id)))
```

Esto generará una tabla HTML con los datos del usuario usando clases de Bootstrap (`table`, `datatable`).

---

## 🔁 Vistas Parciales

Usadas para actualizar fragmentos específicos del DOM con HTMX.

Ejemplo:
```python
def user_row(user):
    return Tr(Td(user.name), Td(user.email))
```

Se puede usar para renderizar dinámicamente solo una fila tras una actualización.

---

## 🧰 Componentes Reutilizables

### 📋 Formulario

Archivo: `components/forms.py`

```python
def user_form(user):
    with Form("/users/update", method="post"):
        Input(_name="name", _value=user.name)
        Input(_name="email", _value=user.email)
```

### 🔘 Botones

Archivo: `components/buttons.py`

```python
def edit_button(id):
    return Button("Editar", _class="btn btn-primary", hx_get=f"/users/edit/{id}", hx_target="#modal-body")
```

Esto mantiene las vistas limpias, DRY (Don't Repeat Yourself) y consistentes.

---

## 🪟 Modales

Muy utilizados en FastApp para cargar formularios dentro de la página sin recargar.

Ejemplo en `clients_views.py`:
```python
def modal_edit(client):
    with Modal("Editar Cliente"):
        forms.client_form(client)
```

El HTML generado se envía como respuesta a una petición HTMX y se inyecta en el modal abierto.

---

## 🪜 Modales Anidados

Un cliente puede tener varios contactos, y es posible editarlos desde el mismo modal del cliente.

Esto se implementa llamando a `contacts_views.list_inline(client_id)` dentro del modal del cliente.

---

## 📦 Layout y Utilidades

En `views/utils.py` se definen funciones de layout reutilizables como encabezados, tarjetas (`Card`), contenedores, etc., que normalizan la estructura visual de las páginas.

---

## 🎯 Conclusión

Gracias a `fasthtml`:
- Las vistas son 100% Python.
- El frontend se mantiene cerca del backend.
- Se puede depurar, mantener y escalar de manera más simple.
- Se aprovecha al máximo la lógica condicional y estructural del lenguaje.

FastApp demuestra cómo `fasthtml` puede reemplazar plantillas HTML tradicionales con una solución moderna y Pythonic.
