# Chapter 3 - Project Structure

The structure of the FastApp project is organized to follow the **MVC** pattern (Model - View - Controller), which allows for a clear separation of business logic, presentation, and data access.

Below is a description of the contents and purpose of each folder:

```
fastapp/
├── main.py
├── .env
├── fastdata.db
├── src/
│   ├── auth/
│   ├── controllers/
│   ├── core/
│   ├── data/
│   ├── utils/
│   └── views/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
```

### `main.py`
Main file that initializes the application. It imports the controllers and calls their `init_routes()` methods to register routes.

```python
from src.controllers.clients_controller import ClientsController
ClientsController().init_routes(rt)
```

### `src/auth/`
Contains authentication logic such as credential verification (`login.py`).

### `src/controllers/`
Defines the application's routes and control logic. Each controller manages a specific entity.

Example:
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

    def list(self, session, request):
        try:
            users = UserDAO().get_all(order_by={"username": "ASC"})
            return users_page(session, users)
        except Exception as e:
            return error_msg(f"ERROR: {e}")
    ...
```

### `src/core/`
Functions that encapsulate shared logic, such as HTML wrappers (`html_wrappers.py`) compatible with fasthtml.  
This utility allows customizing the design of fast-tags (`ft`) for each application.

### `src/data/`
Contains data models and DAOs. It also includes the SQLAlchemy setup and data validation utilities.

- `models.py`: Base model classes using SQLAlchemy  
- `validators.py`: Utilities used for data validation  
- `database.py`: Database connection (SQLite in this example)

### `src/views/`
Views are built with `fasthtml`. Each file defines functions that generate structured HTML using Python.

Example:
```python
def users_page(session, users, user_id:int=0, hx_swap_oob:bool=False):
    return \
    Div(
        users_navbar(session),
        Div(id="user-modals-here", hx_swap_oob="true" if hx_swap_oob else "")(""),
        Div(id="users-list", hx_swap_oob="true" if hx_swap_oob else "")(
            users_list(session, users, user_id=user_id),
        )
    )
```

### `src/utils/`
Helper functions such as Excel export (`excel.py`), JavaScript scripts, and HTMX integration.

### `static/`
Contains static resources accessible from the browser:
- Custom CSS
- JavaScript for interactivity
- Icons and animations

This modular structure helps keep the project organized, testable, and easy to extend.

---