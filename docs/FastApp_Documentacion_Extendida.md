# 📘 Documentación Técnica Detallada del Proyecto FastApp

---

## 1. Introducción

**FastApp** es una aplicación web desarrollada en Python, que utiliza la innovadora librería `fasthtml` para construir dinámicamente interfaces HTML desde el servidor, sin necesidad de plantillas tradicionales. La aplicación implementa un sistema de gestión de usuarios, clientes y sus respectivos contactos. Está orientada a entornos administrativos o CRM sencillos, con una experiencia de usuario altamente interactiva, impulsada por el uso de HTMX, Bootstrap, JavaScript y modales anidados.

Esta documentación detalla todos los aspectos técnicos del proyecto, con referencias específicas al código, arquitectura, diseño, lógica, tecnologías utilizadas e instrucciones para su despliegue.

---

## 2. Características Principales (Features)

FastApp cuenta con las siguientes funcionalidades clave:

### ✅ Gestión de usuarios
- Controladores: `src/controllers/users_controller.py`
- Vistas: `src/views/users_views.py`
- DAO: `src/data/DAO_users.py`
- Permite listar, agregar, editar y eliminar usuarios.

### 📇 Gestión de clientes y contactos
- Clientes:
  - Controlador: `clients_controller.py`
  - Vista: `clients_views.py`
  - DAO: `DAO_clients.py`
- Contactos:
  - Anidados dentro del cliente.
  - Controlador: `contacts_controller.py`
  - Vistas: `contacts_views.py`

### 🔐 Autenticación y sesiones
- Lógica en: `src/auth/login.py` y `login_controller.py`
- Validación y persistencia de sesión con tokens (`.sesskey`)

### 📤 Exportación a Excel
- Función en: `src/utils/excel.py`
- Permite exportar cualquier tabla visible a `.xlsx`

### ⚡ Interactividad HTMX
- Código JS: `src/utils/htmx.py`, `static/js/main.js`
- Se usa para actualizar secciones del DOM sin recargar página

### 🪟 Edición con modales
- Están definidos en las vistas (ej. `users_views.py`, `clients_views.py`)
- Implementan acciones como editar datos sin salir del contexto

### 🪜 Modales anidados
- Contactos de un cliente se editan dentro de un modal secundario.
- Lógica dispersa entre `clients_views.py` y `contacts_views.py`

---

## 3. Estructura del Proyecto

Organización general del repositorio:

```
fastapp/
├── main.py
├── .env
├── src/
│   ├── auth/
│   ├── controllers/
│   ├── core/
│   ├── data/
│   ├── utils/
│   └── views/
├── static/
└── fastdata.db
```

### Explicación de carpetas:
- `src/auth`: Autenticación y manejo de sesión.
- `src/controllers`: Controladores que procesan peticiones.
- `src/data`: Acceso a datos, modelos, validaciones.
- `src/views`: Generación de interfaces HTML con `fasthtml`.
- `src/utils`: Funciones auxiliares como exportación o scripts JS.
- `static/`: Recursos estáticos (CSS, JS, imágenes).

---

## 4. Tecnologías y Enfoques Técnicos

FastApp combina distintas tecnologías para enriquecer la experiencia con `fasthtml`:

### 🎨 CSS y Bootstrap
- Archivo principal: `static/css/styles.css`
- Se usa Bootstrap (clases como `btn`, `modal`, `table`) para estilos rápidos.
- Modales y layout responsive están basados en su grid.

### 📊 DataTables.js
- Agregado en `main.js`
- Convierte las tablas HTML (`<table class="datatable">`) en componentes interactivos con búsqueda, orden y paginación.

### 🧱 Modelo MVC
- `controllers/`: Lógica y coordinación.
- `views/`: Representación visual (UI).
- `data/`: Acceso a datos y validaciones.

### 🧠 Integración JS con fasthtml
- Funciones JS como `triggerModal`, `submitForm()` se usan en conjunto con elementos generados por `fasthtml`.
- En `views/utils.py` y `utils/js_scripts.py`

### 🪟 Modales para edición
- Vistas como `users_views.py` generan interfaces con `with Modal(...)` que contienen formularios.
- Creados con componentes de `views/components/forms.py`

### 🪜 Modales dentro de modales
- En `clients_views.py`, se incluye la vista `contacts_views.show(...)` dentro de un modal secundario.
- Manejo cuidadoso del contexto con HTMX.

---

## 5. Configuración y Entorno

- Variables definidas en `.env`, como `SECRET_KEY`
- Librerías utilizadas:
  - `fasthtml`
  - `openpyxl` (para Excel)
  - `sqlite3`
  - `python-dotenv`

### Requisitos
- Python 3.12+
- Paquetes instalables vía `requirements.txt` (generable con `pip freeze`)

---

## 6. Flujo de Ejecución

1. **main.py** lanza la aplicación con `from fasthtml import app`
2. Se registra cada vista/controlador mediante `@route()`
3. El controlador gestiona la lógica y llama a la vista
4. La vista construye la interfaz con `fasthtml`
5. La respuesta es devuelta como HTML al cliente

---

## 7. Base de Datos

- Base: SQLite (`fastdata.db`)
- ORM simplificado basado en clases DAO

### DAOs y Modelos:
- `DAO_users.py`, `DAO_clients.py`, `DAO_contacts.py`
- `models.py`: clases base que representan las entidades
- `table_DAO.py`: lógica CRUD común para cualquier tabla

---

## 8. Sistema de Autenticación

- Formulario login en `login_views.py`
- Validación contra base de datos en `auth/login.py`
- Generación de sesión con hash secreto
- Verificación en cada controlador con decoradores (`@authenticated`)

---

## 9. Sistema de Vistas

- Todas las vistas están en `views/`
- Compuestas con `fasthtml` usando sintaxis Python:
  ```python
  with Div():
      H1("Bienvenido")
      Button("Acceder", _class="btn btn-primary")
  ```

- Componentes reutilizables:
  - Formularios: `components/forms.py`
  - Botones: `components/buttons.py`

---

## 10. Integraciones

- 📤 **Excel**: `utils/excel.py` usa `openpyxl` para generar archivos Excel desde listas de diccionarios.
- 🧠 **HTMX**: se usa para cargar contenidos parcialmente (`hx-get`, `hx-target`)
- ⚙️ **JS scripts**: `main.js`, `js_scripts.py`

---

## 11. Estilos y Recursos Estáticos

- `modals.css`: estilos específicos para modales
- `styles.css`: apariencia general
- `img/`: íconos SVG usados en animaciones o botones

---

## 12. Pruebas y Generación de Datos

- Script `__create_data.py` llena la base de datos con usuarios, clientes y contactos de ejemplo.
- Útil para demos y pruebas rápidas.

---

## 13. Licencia y Créditos

- Licencia MIT (ver archivo LICENSE)
- Creado con `fasthtml`, un proyecto de código abierto por Answer.AI

---

## 14. Instrucciones para Ejecutar la App

```bash
git clone <repo>
cd fastapp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---
