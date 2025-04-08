# Chapter 6 - Execution Flow

The execution flow in FastApp follows a logical structure based on the MVC (Model-View-Controller) pattern, with route integration through classes and HTML rendering using `fasthtml`. Below is a step-by-step description of what happens from the moment the application starts until a user request is served.

---

## 🚀 1. Application Startup

The application starts execution in the `main.py` file.

### What happens here?

- The `app` instance is imported from `fasthtml`, and the `app` is launched.
- Routes are initialized from the controllers using `init_routes(rt)`.
- The local server is started using `serve` or `uvicorn`.
- For production, it's recommended to use `uvicorn` as shown in `main.py`.

---

## 🌐 2. HTTP Request from the Client

When a user accesses the application from a browser (e.g., `http://localhost:5001/users`), a GET request is triggered to the server.

---

## 🧭 3. Routing via `init_routes()` in Controller Classes

Each controller defines routes using a `Controller` class instead of the `@rt()` decorator,  
which allows splitting code across different files rather than concentrating everything in `main.py`.

Example from `users_controller.py`:
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
```

- `rt` is the routing context passed from the `app`.
- The database is queried using a DAO.
- An HTML view is returned using `fasthtml`.

---

## 🛠️ 4. Controller Logic

Each controller includes functions that define:
- Which route to handle.
- What data to retrieve or modify.
- Which view to return.
- How to validate user input.

---

## 🧩 5. HTML Rendering with fasthtml

HTML rendering is performed using **fasthtml** and its fast-tags (ft), which are used like functions returning the required HTML code.

Example:
```python
def home_page(session, request):
    return Div(cls="container")(
        H1("Home Page"),
        P("A paragraph of text"),
        Ul()(
            Li(cls="text-danger nav-link")("Option 1"),
            Li(cls="text-danger nav-link")("Option 2"),
            Li(cls="text-danger nav-link")("Option 3"),
        )
    )
```

This code:
- Uses nested blocks.
- Applies CSS classes.
- Builds reusable components.

---

## 🔁 6. Client Response

The result is plain HTML sent to the browser, where it is rendered directly.

If the request originated from HTMX (e.g., clicking an edit button), only a portion of the DOM is updated thanks to attributes like `hx-target` and `hx-swap`.

---

## 🔒 7. Authentication Verification

Using functions and decorators defined in `src/auth/login.py`, such as:
- `login_required()`
- `user_role_required()`
- `is_user_logged()`
- `get_user_info()`
- `is_user_admin()`

Access to different parts of the app can be customized depending on whether a user is logged in or based on their role.

This system relies on the `session` object, a dictionary that stores data accessible from the application's routes.

---

## 🔄 8. Interactivity

When actions are performed such as:
- Submitting a form
- Opening a modal
- Editing a table

Everything happens through controlled route calls, and partial views are updated using HTMX. Entire pages are not reloaded—only DOM fragments.

---

## ✅ Full Flow Example (editing a user)

1. User clicks "Edit" → triggers `hx-get="/users/edit/5"`.
2. `form_edit()` is executed in `users_controller.py`.
3. The modal is generated in `users_views.users_form()`.
4. The partial HTML is injected into the modal (`#user-modals-here`).
5. User edits the data and submits the form → `hx-post="/users_post"`.
6. `process_post` is executed and the database is updated.
7. The user table is reloaded via HTMX.

---

This clear and organized flow simplifies maintenance, debugging, and scaling of the project.

---