# Chapter 9 - View System

The view system in FastApp is built entirely using the `fasthtml` library, which allows generating dynamic and structured HTML interfaces directly from Python code. This approach eliminates the need for traditional HTML templates, promotes stronger code cohesion, and simplifies component reuse.

---

## 🧩 What is fasthtml?

`fasthtml` is a library that transforms Python structures into HTML DOM trees declaratively. It uses a syntax based on nested blocks and HTML-like attributes.

---

## 🏗️ View Organization

Views are located in `src/views/` and are organized by entity:

- `users_views.py`: views for users  
- `clients_views.py`: views for clients  
- `contacts_views.py`: views for client contacts  
- `home_views.py`: views for the homepage and for non-logged-in users  
- `login_views.py`: views related to the login system  
- `components/`: reusable buttons and forms  
- `utils.py`: common rendering functions  

---

## 🔁 Reusable Components

### 📋 Form Fields

File: `components/forms.py`

Contains functions used to generate form fields:
- `mk_input()`: generates general `<INPUT>` tags  
- `mk_select()`: generates `<SELECT>` tags  
- `mk_textarea()`: generates `<TEXTAREA>` tags  
- `mk_date()`: generates date input fields, including dropdown calendars  
- `mk_number()`: specialized input for numeric formats  
- `mk_currency()`: specialized input for currency formats (€ , $, etc.)

### 🔘 Buttons

File: `components/buttons.py`

Contains button-related code, currently:
- `rowButton()`: a button used in table rows to edit or delete the displayed record.

This keeps views clean, DRY (Don't Repeat Yourself), and consistent.

---

## 🪟 Modals

Used for editing records. They are triggered and dismissed using HTMX.  
They help improve user interaction and interface fluidity.

---

## 🪜 Nested Modals

This application demonstrates an example of nested modals for clients and contacts.  
A client can have multiple contacts, and they can be edited directly from within the client modal.

---

## 📦 Utilities

In `views/utils.py`, reusable layout functions are defined, such as:
- `error_msg()`: displays an error inside a `<DIV>`  
- `format_currency()`: displays a numeric value as a currency  

---

## 🎯 Conclusion

Thanks to `fasthtml`:
- Views are 100% Python.  
- Frontend remains close to the backend.  
- Debugging, maintenance, and scaling are simpler.  
- Python’s structural and conditional logic is fully leveraged.  

FastApp demonstrates how `fasthtml` can replace traditional HTML templates with a modern and Pythonic solution.

---