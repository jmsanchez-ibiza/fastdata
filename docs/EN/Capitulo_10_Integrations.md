# Chapter 10 - Integrations

FastApp extends its basic functionalities through various integrations that enhance the user experience, enable data export, and add interactivity without overloading the frontend with heavy frameworks. These integrations include tools such as Excel export, custom JavaScript, and HTMX.

---

## 📤 1. Excel Export

Implemented in `src/utils/excel.py` using the `openpyxl` library.

---

## ⚙️ 2. Custom JavaScript

In `static/js/main.js` and `src/utils/js_scripts.py`, you’ll find functions to:

- Initialize DataTables  
- Display modals  
- Capture button events  

---

## 🔁 3. HTMX

HTMX is key to achieving interactivity without reloading the entire page.

---

## 🧩 4. Modal Integration

The `fasthtml` modal system is integrated with JS and HTMX. The modal structure is defined in Python, but its opening and closing are handled via JS or `hx` attributes.

---

## 🖼️ 5. Static Assets

FastApp includes additional resources to improve the visual presentation:

- **SVG icons**: located in `static/img/`  
- **Custom CSS**: in `static/css/styles.css` and `modals.css`  
- **Animations**: such as loading spinners used in the `Save` button of data editing modals, in case the operation takes time  

---

## 💡 Summary

FastApp’s integrations enable it to:

- Export data in useful formats like Excel  
- Deliver a smooth UX with HTMX  
- Incorporate lightweight JS components without heavy frameworks  
- Leverage modals as dynamic containers for forms  

These tools enhance the functionality of an application that, while structurally simple, offers a powerful and modern user experience.

---