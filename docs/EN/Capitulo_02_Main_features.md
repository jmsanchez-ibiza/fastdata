# Chapter 2 - Main Features

FastApp includes multiple functionalities that enable a smooth user experience and a scalable architecture:

### ✅ User Management
- Route: `users_controller.py`
- View: `users_views.py`
- DAO: `DAO_users.py`

Supports full CRUD operations and filtering.

### 📇 Client and Contact Management
- Clients: `clients_controller.py`, `clients_views.py`
- Contacts: `contacts_controller.py`, `contacts_views.py`

Contacts are hierarchically related to clients and can be edited either from their own view or from within the client’s modal.

### 🔐 Authentication and Sessions
- `auth/login.py` handles credential validation.
- `login_controller.py` manages the login form.

### 📤 Excel Export
- Implemented in `utils/excel.py` using `openpyxl`.
- The `export_to_excel` function converts lists of dictionaries into `.xlsx` files.
- Serves as an example of both exporting data to Excel and creating a file download button.

### ⚡ Interactivity with HTMX
- Used throughout the app (`hx-get`, `hx-target`, `hx-swap`).
- Improves the user experience by only loading fragments of the DOM.
- The app is structured as a SPA (Single Page Application), focused on a main page where content is dynamically loaded into the DOM.

### 🪟 Use of Modals
- CRUD forms and actions are presented in modal windows, defined with `fasthtml`.

### 🪜 Nested Modals
- Example: From a client modal, a contact modal can be opened without losing context.

### 🔁 Modular Routing with `init_routes()`
- Each `controllers/*_controller.py` file defines a class with an `init_routes()` method.
- These classes are imported from `main.py`, helping to organize the routing logic:

```python
from src.controllers.clients_controller import ClientsController

ClientsController().init_routes(rt)
```

This allows for a clear division of routing logic without cluttering the entry file (`main.py`).  
It makes the code more readable and easier to maintain by splitting it across multiple `.py` files.

### 🗃️ SQLAlchemy as the ORM for the Database
FastApp uses the `SQLAlchemy` library to manage the SQLite database. Thanks to this:

- The database engine can be easily switched to **PostgreSQL**, **MySQL**, or **MariaDB** without changing the data logic.
- The model definitions in `src/data/models.py` define entities as Python classes.
- The DAOs (`DAO_clients.py`, `DAO_users.py`, etc.) operate on these classes to perform CRUD operations.

This makes the project **portable, modular, and scalable** for more demanding production environments.

---
