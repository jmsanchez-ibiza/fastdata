# Capítulo 10 - Integraciones

FastApp amplía sus funcionalidades básicas mediante diversas integraciones que mejoran la experiencia del usuario, permiten exportar datos y añaden dinamismo sin sobrecargar el frontend con frameworks pesados. Estas integraciones incluyen herramientas como Excel, JavaScript personalizado, y HTMX.

---

## 📤 1. Exportación a Excel

Implementado en `src/utils/excel.py` utilizando la librería `openpyxl`.

### Función principal:
```python
def export_to_excel(data, filename="export.xlsx"):
    wb = Workbook()
    ws = wb.active
    headers = data[0].keys()
    ws.append(headers)
    for row in data:
        ws.append(list(row.values()))
    wb.save(filename)
```

### ¿Cómo se usa?
Desde un controlador, se llama a esta función pasando los datos:
```python
@route("/users/export")
def export_users(ctx):
    data = [user.as_dict() for user in DAOUsers().get_all()]
    return export_to_excel(data, "usuarios.xlsx")
```

Esto genera un archivo descargable con el contenido actual de la base de datos.

---

## ⚙️ 2. JavaScript Personalizado

En `static/js/main.js` y `src/utils/js_scripts.py` se encuentran funciones para:

- Inicializar DataTables
- Mostrar modales
- Capturar eventos de botones

### Ejemplo de inicialización:
```javascript
$(document).ready(function () {
  $('.datatable').DataTable();
});
```

### Ejemplo de función para recargar una tabla:
```javascript
function reloadUsersTable() {
    htmx.ajax('GET', '/users', '#main-container');
}
```

---

## 🔁 3. HTMX

HTMX es clave para lograr interactividad sin recargar la página completa.

### Uso típico en vistas con `fasthtml`:
```python
Button("Editar", hx_get=f"/users/edit/{user.id}", hx_target="#modal-body", hx_swap="innerHTML")
```

### ¿Qué hace?
- Hace una petición GET a `/users/edit/{id}`
- Inyecta la respuesta HTML en el `#modal-body`
- Evita redireccionamientos y refrescos de página

---

## 🧩 4. Integración con Modales

El sistema de modales de `fasthtml` está integrado con JS y HTMX. Se define la estructura del modal en Python, pero su apertura y cierre se manejan desde JS o atributos `hx`.

Ejemplo de apertura:
```html
<button hx-get="/clients/edit/3" hx-target="#modal-body" data-bs-toggle="modal" data-bs-target="#modal">
    Editar Cliente
</button>
```

---

## 🖼️ 5. Recursos Estáticos

FastApp incluye recursos adicionales para mejorar la presentación:

- **Íconos SVG**: ubicados en `static/img/`
- **CSS personalizado**: en `static/css/styles.css` y `modals.css`
- **Animaciones**: como spinners para cargar contenido dinámico

---

## 💡 En resumen

Las integraciones de FastApp le permiten:

- Exportar datos en formatos útiles como Excel
- Ofrecer una experiencia fluida con HTMX
- Incorporar componentes JS ligeros sin frameworks pesados
- Aprovechar modales como contenedores dinámicos de formularios

Estas herramientas amplifican la funcionalidad de una aplicación que, a pesar de su sencillez estructural, ofrece una experiencia potente y moderna.
