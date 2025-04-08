# Capítulo 12 - Pruebas y Generación de Datos

FastApp incorpora un mecanismo sencillo pero funcional para poblar la base de datos con información de prueba. Esto facilita la verificación del sistema, demostraciones y desarrollo sin necesidad de ingresar manualmente los datos desde la interfaz.

---

## 🧪 Script de Datos de Prueba

El archivo `__create_data.py` es el encargado de crear:

- Las tablas necesarias en la base de datos
- Un conjunto de usuarios, clientes y contactos de prueba

---


## 🧰 Cómo usarlo

Simplemente ejecutar:

```bash
python __create_data.py
```

Esto:
- Borra cualquier contenido previo (si se ha configurado así).
- Rellena la base de datos `fastdata.db` con registros listos para probar.

---


## 🎯 Utilidad

- Ideal para demostraciones en tiempo real
- Útil al iniciar el proyecto por primera vez
- Facilita pruebas de formularios, modales y tablas

---

## 🛡️ Consideraciones

- Este script está pensado para entornos de desarrollo.
- No debe ejecutarse en producción sin ajustes.
- Se puede extender para crear fixtures o datos aleatorios.

---

En resumen, `__create_data.py` es una herramienta útil para acelerar el ciclo de desarrollo y garantizar que la aplicación tenga siempre datos con los que trabajar al instante.
