# Capítulo 9 - Sistema de Vistas

El sistema de vistas en FastApp está construido íntegramente con la librería `fasthtml`, que permite generar interfaces HTML dinámicas y estructuradas directamente desde código Python. Esta aproximación elimina la necesidad de plantillas HTML tradicionales, lo que favorece una mayor cohesión del código y facilita la reutilización de componentes.

---

## 🧩 ¿Qué es fasthtml?

`fasthtml` es una librería que transforma estructuras Python en árboles DOM HTML de forma declarativa. Usa una sintaxis de bloques anidados y atributos similares a los del HTML.

---

## 🏗️ Organización de Vistas

Las vistas se encuentran en `src/views/` y están organizadas por entidad:

- `users_views.py`: vistas para usuarios.
- `clients_views.py`: vistas para clientes.
- `contacts_views.py`: vistas para contactos de clientes.
- `home_views.py`: vistas para la página home y de acceso a usuarios no loggeados.
- `login_views.py`: vistas relacionadas con el sistema de login.
- `components/`: botones y formularios reutilizables
- `utils.py`: funciones de renderizado comunes

---

## 🔁 Componentes Reutilizables

### 📋 Formulario

Archivo: `components/forms.py`

Contiene las funciones utilizadas para la generación de campos en los formularios:
- mk_input(): genera los tags <INPUT> generales.
- mk_select(): genera los tags <SELECT>.
- mk_textarea(): genera los tags para <TEXTAREA>.
- mk_date(): genera los tags para el input de datos tipo fecha, incluso calendario desplegable.
- mk_number(): genera un input especializado en manejar formatos numéricos.
- mk_currency(): genera un input especializado en manejar formatos numéricos de moneda (€, $, etc)

### 🔘 Botones

Archivo: `components/buttons.py`

Contiene el código relacionado con botones, actualmente sólo:
- rowButton(): botón usado en las filas de las tablas para editar o borrar el registro mostrado.

Esto mantiene las vistas limpias, DRY (Don't Repeat Yourself) y consistentes.

---

## 🪟 Modales

Se usan en la edición de los registros. Se invocan y destruyen mediante HTMX.
Facilitan la interface con el usuario.

---

## 🪜 Modales Anidados

En esta aplicación se muestra un ejemplo de modales anidados cliente-contactos.
Un cliente puede tener varios contactos, y es posible editarlos desde el mismo modal del cliente.

---

## 📦 Utilidades

En `views/utils.py` se definen funciones de layout reutilizables como:
- error_msg(): para mostrar un error dentro de un <DIV>
- format_currency(): para mostrar un dato numérico tipo moneda.

---

## 🎯 Conclusión

Gracias a `fasthtml`:
- Las vistas son 100% Python.
- El frontend se mantiene cerca del backend.
- Se puede depurar, mantener y escalar de manera más simple.
- Se aprovecha al máximo la lógica condicional y estructural del lenguaje.

FastApp demuestra cómo `fasthtml` puede reemplazar plantillas HTML tradicionales con una solución moderna y Pythonic.
