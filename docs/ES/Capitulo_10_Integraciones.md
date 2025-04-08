# Capítulo 10 - Integraciones

FastApp amplía sus funcionalidades básicas mediante diversas integraciones que mejoran la experiencia del usuario, permiten exportar datos y añaden dinamismo sin sobrecargar el frontend con frameworks pesados. Estas integraciones incluyen herramientas como Excel, JavaScript personalizado, y HTMX.

---

## 📤 1. Exportación a Excel

Implementado en `src/utils/excel.py` utilizando la librería `openpyxl`.

## ⚙️ 2. JavaScript Personalizado

En `static/js/main.js` y `src/utils/js_scripts.py` se encuentran funciones para:

- Inicializar DataTables
- Mostrar modales
- Capturar eventos de botones

## 🔁 3. HTMX

HTMX es clave para lograr interactividad sin recargar la página completa.

---

## 🧩 4. Integración con Modales

El sistema de modales de `fasthtml` está integrado con JS y HTMX. Se define la estructura del modal en Python, pero su apertura y cierre se manejan desde JS o atributos `hx`.

---

## 🖼️ 5. Recursos Estáticos

FastApp incluye recursos adicionales para mejorar la presentación:

- **Íconos SVG**: ubicados en `static/img/`
- **CSS personalizado**: en `static/css/styles.css` y `modals.css`
- **Animaciones**: como spinners para cargar contenido dinámico, usado en el botón `Save` de los modales de edición de datos, por si se retrasa el trabajo.

---

## 💡 En resumen

Las integraciones de FastApp le permiten:

- Exportar datos en formatos útiles como Excel
- Ofrecer una experiencia fluida con HTMX
- Incorporar componentes JS ligeros sin frameworks pesados
- Aprovechar modales como contenedores dinámicos de formularios

Estas herramientas amplifican la funcionalidad de una aplicación que, a pesar de su sencillez estructural, ofrece una experiencia potente y moderna.
