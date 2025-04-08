# 📘 Documentación del Proyecto FastApp

## 1. Introducción

FastApp es una aplicación web construida en Python utilizando la librería **fasthtml**. Su objetivo es ofrecer es mostar todas las posibilidades de **fasthtml**, mediante el desarrollo de una aplicación web interactiva para la gestión de usuarios, clientes y contactos, con una interfaz web dinámica y responsiva.

## 2. Características Principales

- ✅ Gestión de usuarios con control de acceso.
- 📇 Gestión jerárquica de clientes y sus contactos.
- 🔐 Sistema de autenticación y sesiones.
- 📤 Exportación de datos a archivos Excel.
- ⚡ Interactividad mediante HTMX.
- 🧩 Interfaz HTML modular construida con `fasthtml`.
- 🪟 Uso de modales para edición y navegación contextual.
- 🔄 Soporte para modales anidados (ej: contactos dentro de clientes).
- 💾 Gestión de la base de datos mediante `SqlAlchemy`, de manera que es escalable desde SQLite a otras bases de datos como MySQL, PostgreSQL, etc.

## 3. Estructura del Proyecto

```
fastapp/
├── main.py                # Punto de entrada
├── .env                   # Variables de entorno
├── fastdata.db            # Base de datos SQLite
├── src/                   # Código fuente principal
│   ├── config.py
│   ├── auth/              # Autenticación
│   ├── controllers/       # Controladores (Capa lógica)
│   ├── core/              # Funciones HTML y envoltorios
│   ├── data/              # Modelos, DAOs, validaciones
│   ├── utils/             # Utilidades (Excel, JS, etc.)
│   └── views/             # Vistas construidas con fasthtml
└── static/                # Recursos estáticos (CSS, JS, imágenes)
```

## 4. Tecnologías y Enfoques Técnicos

- 🎨 **CSS personalizado + Bootstrap** para un diseño limpio y responsivo.
- 📊 **DataTables.js** para visualización interactiva de tablas.
- 🧱 **Arquitectura MVC**: separación clara entre modelos, vistas y controladores.
- 🧠 **Integración de JavaScript** embebido y dinámico con `fasthtml`.
- 🪟 **Modales personalizados** para edición inline sin navegación adicional.
- 🪜 **Modales dentro de modales**, como la edición de contactos dentro de un cliente.
- 🔁 **HTMX** para recarga parcial de vistas y una UX fluida.
- 💾 Gestión de la base de datos mediante `SqlAlchemy`

## 5. Configuración y Entorno

- Variables de entorno definidas en `.env`
- Requiere Python 3.12+
- Librerías: `fasthtml`, `openpyxl`, `sqlite3`, `htmx`, `sqlalchemy`, entre otras.

## 6. Flujo de Ejecución

1. El usuario accede a través de `main.py`.
2. Se enruta a un controlador correspondiente.
3. El controlador interactúa con los DAOs.
4. Se genera una vista dinámica con `fasthtml`.
5. El navegador actualiza el contenido con HTMX.

## 7. Base de Datos

- Base de datos: `SQLite`
- Modelos en `data/models.py`
- DAOs (Data Access Objects) en: `DAO_users.py`, `DAO_clients.py`, `DAO_contacts.py`
- Acceso abstracto con `table_DAO.py`

## 8. Sistema de Autenticación

- Módulo `auth/login.py`
- Login mediante formulario con validación de sesión
- Protección de rutas con verificación en cada controlador mediante decoradores

## 9. Sistema de Vistas

- Vistas creadas con `fasthtml` en módulos `views/`
- Componentes reutilizables: botones (`components/buttons.py`), formularios (`components/forms.py`)
- Código HTML generado dinámicamente

## 10. Integraciones

- 📁 Exportación de datos a Excel en `utils/excel.py`
- ⚙️ Scripts auxiliares JS en `utils/js_scripts.py`
- 🌩️ Eventos y acciones con HTMX (`utils/htmx.py`)

## 11. Estilos y Recursos Estáticos

- CSS en `static/css/`
- JS en `static/js/main.js`
- Imágenes: íconos de carga y acciones (`static/img/`)

## 12. Pruebas y Generación de Datos

- Script `__create_data.py` para poblar la base de datos con datos de prueba

## 13. Licencia y Créditos

Este proyecto se distribuye bajo la licencia MIT. Ver archivo `LICENSE`.

## 14. Instrucciones para Ejecutar la App

1. Clonar el repositorio.
2. Crear y configurar el entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate en Linux o venv\Scripts\activate.bat en Windows
   pip install -r requirements.txt
   ```
3. Configurar variables en `.env`
4. Ejecutar:
   ```bash
   python main.py
   ```

---
