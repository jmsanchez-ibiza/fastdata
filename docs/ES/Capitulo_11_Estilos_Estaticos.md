# Capítulo 11 - Estilos y Recursos Estáticos

FastApp incorpora recursos estáticos esenciales para ofrecer una interfaz visual atractiva, funcional y responsiva. Estos recursos están organizados en la carpeta `static/`, que incluye archivos CSS, JavaScript y diversas imágenes utilizadas en la interfaz.

---

## 🎨 1. Archivos CSS

Ubicados en: `static/css/`

### `styles.css`
Contiene reglas personalizadas para adaptar elementos como botones, tablas y formularios a la estética del proyecto.


### `modals.css`
Contiene estilos específicos para mejorar el comportamiento visual de los modales creados con en la aplicación.

---

## 💡 2. Imágenes y Recursos Visuales

Ubicadas en: `static/img/`

FastApp utiliza íconos SVG y PNG que se muestran en botones, cabeceras o durante la carga de contenido.

### Imágenes comunes:
- `spin-200px.svg`: Spinner animado
- `recycle.png`: Icono de la aplicación.
- `bars-spinner.svg`, `ring-spinner.svg`: Variantes visuales para carga o espera

---

## ⚙️ 3. Archivos JavaScript

Ubicados en: `static/js/`

### `main.js`
Contiene inicializadores de componentes como DataTables y funciones que ayudan a manejar eventos interactivos.

Ejemplo:
```javascript
$(document).ready(function () {
  $('.datatable').DataTable();
});
```

Incluye también funciones para:
- Recargar partes del DOM
- Mostrar u ocultar elementos
- Activar/desactivar botones

---

## 🧩 4. Uso en Vistas y Componentes

Los archivos estáticos se enlazan automáticamente a través del sistema de rutas de `fasthtml` desde `main.py`

Esto asegura que todos los elementos visuales y scripts estén disponibles cuando se genera una vista.

---

## 📁 Estructura de la Carpeta `static/`

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

## 🧠 Buenas prácticas

- Se mantiene la separación entre lógica y presentación.
- Los archivos estáticos son independientes del motor de vistas.
- Fácil de reemplazar o extender (por ejemplo, incorporar un framework como Tailwind o cambiar de Bootstrap a Bulma).

---

Este sistema de archivos estáticos bien estructurado permite a FastApp mantener una experiencia de usuario coherente y moderna.
