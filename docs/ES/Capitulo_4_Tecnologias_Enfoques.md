# Capítulo 4 - Tecnologías y Enfoques Técnicos

FastApp utiliza una combinación de tecnologías modernas y patrones de diseño que potencian el desarrollo modular y mantenible de la aplicación. A continuación, se detallan las herramientas y enfoques más relevantes:

---

## 🧱 1. fasthtml
La librería central del proyecto, permite construir interfaces HTML directamente desde código Python.

Ejemplo desde `users_views.py`:
```python
def users_list(session, users, user_id:int=0, hx_swap_oob:bool=False):

    return Table(
        id="users-table",
        data_page_length="10",
        cls="table table-striped table-hover display compact datatable",  # datatable, is the required class to transform it into a DataTable.
        style="width: 100%; background-color: white;",
        )(
        Thead(
            Tr(
                Th(scope="col")("🛠️"),
                Th(scope="col")("Id/Code"),
                Th(scope="col")("Username"),
                Th(scope="col")("Name"),
                Th(scope="col")("Role"),
            )
        ),
        Tbody()(
            *[user_row(session, user, user_id = user_id) for user in users]
        ),
        Tfoot(
            Tr(
                Th(scope="col", cls="dt-orderable-asc")("🛠️"),
                Th(scope="col", cls="dt-orderable-asc")("Id/Code"),
                Th(scope="col", cls="dt-orderable-asc")("Username"),
                Th(scope="col", cls="dt-orderable-asc")("Name"),
                Th(scope="col", cls="dt-orderable-asc")("Role"),
            )
        ),
    ) if users else Div(H5(cls="text-center text-danger pt-3")("No users found"))

    ...
```

Ventajas:
- No se utilizan plantillas HTML (como en el caso de Flask o Django con Jinja2).
- Todo el contenido HTML está definido de forma estructurada en Python.
- Reutilización de componentes, mediante funciones o clases.

---

## 🎨 2. Inegración con Bootstrap (CSS)
Mediante el uso de Script() y Link(), se puede integrar en las páginas generadas el estilo de este conococido
framework de CSS, para crear aplicaciónes con interfaces limpias, responsivas y consistentes.
Podemos aprovechar componentes ya diseñados en Bootstrap, como navbars, accordions, etc

---

## 📊 3. DataTables.js
Integración de esta librería JS con **fasthtml**.
Configurado en `main.js` para transformar tablas estáticas en dinámicas, con búsqueda, ordenamiento y paginación.

Ejemplo:
```javascript
$(document).ready(function () {
  $('.datatable').DataTable();
});
```

Las tablas generadas en las vistas se marcan con `class="datatable"` para habilitar esta funcionalidad automáticamente.

---

## 🔁 4. HTMX
Permite la recarga parcial del DOM sin necesidad de JavaScript adicional.

Usado en elementos como:
```python
Button("Editar", hx_get="/users/edit/1", hx_target="#modal-body", hx_swap="innerHTML")
```

Ventajas:
- Fluidez en la navegación.
- Reduce el uso de scripts.
- Mejora la experiencia de usuario con menos carga de red.

---

## 🪟 5. Modales
FastApp está diseñado en torno a modales que encapsulan formularios y acciones.
Lo que permite mejorar el interface con el usuario, centrando su atención y manteniendo la filosofía SPA.

Estos modales se activan y se ocultan mediante HTMX.

---

## 🪜 6. Modales anidados
Una funcionalidad avanzada que permite abrir un segundo modal desde uno ya abierto.

Ejemplo: en la edición de un cliente, se puede abrir un modal secundario para gestionar contactos relacionados sin cerrar el anterior.

Implementación:
- `clients_views.py` incluye `contacts_views.list_inline(client_id)` dentro del contenido del modal.
- Coordinado con `hx-target` y `hx-swap`.

---

## 📚 7. Patrón MVC
FastApp sigue el patrón Modelo-Vista-Controlador:
- **Modelo**: `src/data/models.py` y DAOs.
- **Vista**: `src/views/` con `fasthtml`.
- **Controlador**: `src/controllers/` con rutas y lógica.

Este enfoque mejora la organización del proyecto y facilita pruebas, mantenimiento y escalabilidad.

---

## ⚙️ 8. JavaScript Integrado
Aunque HTMX reduce la necesidad de JS personalizado gracias al uso de HTMX, existen scripts en `static/js/main.js` y `utils/js_scripts.py` para:
- Activar DataTables
- Manejar modales
- Ejecutar acciones dinámicas

---

## 🗃️ 9. SQLAlchemy
La capa de persistencia y gestión de la base de datos utiliza `SQLAlchemy` como ORM:
- Código en `data/models.py`
- Session y conexión en `database.py`

Ventaja: el mismo código puede migrarse fácilmente a PostgreSQL, MySQL, etc.

---

## 💡 En resumen:
El diseño técnico de FastApp permite:
- Rápida construcción de interfaces
- Mínimo código frontend
- Escalabilidad a nivel de datos
- Modularidad clara por entidad y función
