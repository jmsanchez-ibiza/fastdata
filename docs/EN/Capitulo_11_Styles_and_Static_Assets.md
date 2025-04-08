# Chapter 11 - Styles and Static Assets

FastApp includes essential static resources to provide a visually appealing, functional, and responsive user interface. These resources are organized in the `static/` folder, which contains CSS files, JavaScript, and various images used throughout the interface.

---

## 🎨 1. CSS Files

Located in: `static/css/`

### `styles.css`  
Contains custom rules to style elements like buttons, tables, and forms according to the project's design aesthetics.

### `modals.css`  
Contains specific styles to enhance the visual behavior of the modals used in the application.

---

## 💡 2. Images and Visual Resources

Located in: `static/img/`

FastApp uses SVG and PNG icons that appear in buttons, headers, or during content loading.

### Common Images:
- `spin-200px.svg`: Animated spinner  
- `recycle.png`: Application icon  
- `bars-spinner.svg`, `ring-spinner.svg`: Loading or waiting visual variants  

---

## ⚙️ 3. JavaScript Files

Located in: `static/js/`

### `main.js`  
Includes initializers for components such as DataTables and functions that help manage interactive events.

Example:
```javascript
$(document).ready(function () {
  $('.datatable').DataTable();
});
```

It also includes functions to:
- Reload parts of the DOM  
- Show or hide elements  
- Enable or disable buttons  

---

## 🧩 4. Usage in Views and Components

Static files are automatically linked through `fasthtml`’s routing system from `main.py`.

This ensures that all visual elements and scripts are available when a view is generated.

---

## 📁 Folder Structure: `static/`

```
static/
├── css/
│   ├── styles.css
│   └── modals.css
├── js/
│   └── main.js
└── img/
    ├── spin-200px.svg
    ├── bars-spinner.svg
    ├── ring-spinner.svg
    └── recycle.png
```

---

## 🧠 Best Practices

- Maintains a clear separation between logic and presentation.  
- Static files are independent of the view engine.  
- Easy to replace or extend (e.g., by integrating a framework like Tailwind or switching from Bootstrap to Bulma).

---

This well-structured static file system allows FastApp to maintain a consistent and modern user experience.

---