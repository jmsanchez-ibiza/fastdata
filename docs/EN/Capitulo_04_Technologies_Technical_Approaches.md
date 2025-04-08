# Chapter 4 - Technologies and Technical Approaches

FastApp uses a combination of modern technologies and design patterns that support modular and maintainable application development. Below are the most relevant tools and approaches:

---

## 🧱 1. fasthtml  
The core library of the project, it allows building HTML interfaces directly from Python code.

Example from `users_views.py`:
```python
def users_list(session, users, user_id:int=0, hx_swap_oob:bool=False):

    return Table(
        id="users-table",
        data_page_length="10",
        cls="table table-striped table-hover display compact datatable",
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
            *[user_row(session, user, user_id=user_id) for user in users]
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
```

Advantages:
- No HTML templates (like Jinja2 in Flask or Django) are used.
- All HTML content is defined in a structured way using Python.
- Components are reusable via functions or classes.

---

## 🎨 2. Bootstrap Integration (CSS)  
By using `Script()` and `Link()`, you can integrate the styles of this well-known CSS framework into generated pages, enabling clean, responsive, and consistent interfaces.  
You can take advantage of pre-built Bootstrap components like navbars, accordions, etc.

---

## 📊 3. DataTables.js  
This JS library is integrated with **fasthtml**. It is configured in `main.js` to transform static tables into dynamic ones, with features like search, sorting, and pagination.

Example:
```javascript
$(document).ready(function () {
  $('.datatable').DataTable();
});
```

Tables generated in views are marked with `class="datatable"` to automatically enable this functionality.

---

## 🔁 4. HTMX  
HTMX allows partial updates of the DOM without the need for additional JavaScript.

Used in elements like:
```python
Button("Edit", hx_get="/users/edit/1", hx_target="#modal-body", hx_swap="innerHTML")
```

Advantages:
- Smooth navigation.
- Reduces the need for custom scripts.
- Improves user experience with lighter network usage.

---

## 🪟 5. Modals  
FastApp is built around modals that encapsulate forms and actions.  
This enhances user interaction by keeping focus and maintaining a SPA-like experience.

These modals are triggered and dismissed using HTMX.

---

## 🪜 6. Nested Modals  
An advanced feature that allows opening a second modal from within an already open one.

Example: While editing a client, a secondary modal can be opened to manage related contacts without closing the previous one.

Implementation:
- `clients_views.py` includes `contacts_views.list_inline(client_id)` inside the modal’s content.
- Coordinated with `hx-target` and `hx-swap`.

---

## 📚 7. MVC Pattern  
FastApp follows the Model-View-Controller pattern:
- **Model**: `src/data/models.py` and DAOs  
- **View**: `src/views/` using `fasthtml`  
- **Controller**: `src/controllers/` with routes and logic

This approach improves project organization and facilitates testing, maintenance, and scalability.

---

## ⚙️ 8. Integrated JavaScript  
Although HTMX reduces the need for custom JS, there are still scripts in `static/js/main.js` and `utils/js_scripts.py` for:
- Activating DataTables
- Handling modals
- Executing dynamic actions

---

## 🗃️ 9. SQLAlchemy  
The persistence and database management layer uses `SQLAlchemy` as the ORM:
- Model definitions in `data/models.py`
- Session and connection logic in `database.py`

Advantage: the same codebase can be easily migrated to PostgreSQL, MySQL, etc.

---

## 💡 Summary  
FastApp’s technical design enables:
- Rapid interface development  
- Minimal frontend code  
- Scalable data layer  
- Clear modularity by entity and functionality

---