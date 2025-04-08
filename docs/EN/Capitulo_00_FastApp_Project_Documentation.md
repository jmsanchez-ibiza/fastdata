# 📘 FastApp Project Documentation

## 1. Introduction

FastApp is a web application built in Python using the **fasthtml** library. Its goal is to showcase all the possibilities of **fasthtml** through the development of an interactive web application for managing users, clients, and contacts, featuring a dynamic and responsive web interface.

## 2. Main Features

- ✅ User management with access control.
- 📇 Hierarchical management of clients and their contacts.
- 🔐 Authentication and session system.
- 📤 Data export to Excel files.
- ⚡ Interactivity through HTMX.
- 🧩 Modular HTML interface built with `fasthtml`.
- 🪟 Use of modals for contextual editing and navigation.
- 🔄 Support for nested modals (e.g., contacts within clients).
- 💾 Database management using `SqlAlchemy`, making it scalable from SQLite to other databases like MySQL, PostgreSQL, etc.

## 3. Project Structure

```
fastapp/
├── main.py                # Entry point
├── .env                   # Environment variables
├── fastdata.db            # SQLite database
├── src/                   # Main source code
│   ├── config.py
│   ├── auth/              # Authentication
│   ├── controllers/       # Controllers (Logic layer)
│   ├── core/              # HTML functions and wrappers
│   ├── data/              # Models, DAOs, validations
│   ├── utils/             # Utilities (Excel, JS, etc.)
│   └── views/             # Views built with fasthtml
└── static/                # Static resources (CSS, JS, images)
```

## 4. Technologies and Technical Approaches

- 🎨 **Custom CSS + Bootstrap** for a clean and responsive design.
- 📊 **DataTables.js** for interactive table visualization.
- 🧱 **MVC Architecture**: clear separation between models, views, and controllers.
- 🧠 **Embedded and dynamic JavaScript integration** with `fasthtml`.
- 🪟 **Custom modals** for inline editing without page navigation.
- 🪜 **Nested modals**, such as editing contacts within a client modal.
- 🔁 **HTMX** for partial view reloads and smooth UX.
- 💾 Database management using `SqlAlchemy`.

## 5. Environment Setup

- Environment variables defined in `.env`
- Requires Python 3.12+
- Libraries: `fasthtml`, `openpyxl`, `sqlite3`, `htmx`, `sqlalchemy`, among others.

## 6. Execution Flow

1. The user accesses through `main.py`.
2. Request is routed to the appropriate controller.
3. The controller interacts with the DAOs.
4. A dynamic view is generated using `fasthtml`.
5. The browser updates content using HTMX.

## 7. Database

- Database: `SQLite`
- Models in `data/models.py`
- DAOs (Data Access Objects) in: `DAO_users.py`, `DAO_clients.py`, `DAO_contacts.py`
- Abstract access using `table_DAO.py`

## 8. Authentication System

- Module `auth/login.py`
- Login via form with session validation
- Route protection via decorators in each controller

## 9. View System

- Views created with `fasthtml` in the `views/` modules
- Reusable components: buttons (`components/buttons.py`), forms (`components/forms.py`)
- HTML code generated dynamically

## 10. Integrations

- 📁 Data export to Excel in `utils/excel.py`
- ⚙️ JS helper scripts in `utils/js_scripts.py`
- 🌩️ Events and actions with HTMX (`utils/htmx.py`)

## 11. Styles and Static Resources

- CSS in `static/css/`
- JS in `static/js/main.js`
- Images: loading and action icons (`static/img/`)

## 12. Testing and Data Generation

- Script `__create_data.py` to populate the database with test data

## 13. License and Credits

This project is distributed under the MIT license. See the `LICENSE` file.

## 14. Instructions to Run the App

1. Clone the repository.
2. Create and configure the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate (Linux) or venv\Scripts\activate.bat (Windows)
   pip install -r requirements.txt
   ```
3. Configure variables in `.env`
4. Run the application:
   ```bash
   python main.py
   ```

---

