# Capítulo 8 - Sistema de Autenticación

El sistema de autenticación en FastApp se encarga de proteger las rutas sensibles de la aplicación y garantizar que sólo usuarios válidos puedan acceder a ciertas funcionalidades.

Está implementado mediante una combinación de:

- Validación de credenciales
- Generación y verificación de sesiones
- Decoradores para proteger rutas

---

## 🔑 Inicio de Sesión

El formulario de login se encuentra definido en `src/views/login_views.py`:

---

## 🔍 Verificación de Credenciales

Se gestiona en `src/auth/login.py`. Esta lógica busca el usuario en la base de datos y compara el nombre de usuario y la contraseña.
Se usa `hash` para la encriptación de las contraseñas.

> *Nota: en una aplicación real, la columna de contraseña `password` sin encriptar debería ser eliminada y sólo usar la columna `password_hash`.*

---

## 📦 Manejador de Login

En `src/controllers/login_controller.py` se define la lógica del endpoint `/login` y `logout` y `/login_post` (para la comprobación del nombre de usuario y contraseña)

---

## 🔐 Sesiones

- Las sesiones están gestionadas internamente por `fasthtml`.
- El `session` permite almacenar el estado del usuario de forma persistente durante su navegación.

---

## 🚪 Cierre de Sesión

Ruta definida en `login_controller.py` a través de `/logout`
Esto borra toda la sesión del usuario y lo redirige a la pantalla de home.

---

## 🛡️ Protección de Rutas

FastApp utiliza varias funciones alojadas en `src/auth/login.py' para bloquear rutas si el usuario no está logueado o si su 'role' no es el exigido.


---

## 🧪 Datos de Prueba

El script `__create_data.py` genera un usuario con el email y contraseña:
```
Email: admin@example.com
Password: admin
```

---

Este sistema simple pero funcional cubre los requisitos básicos de autenticación para una app administrativa. Puede mejorarse fácilmente con cifrado de contraseñas y expiración de sesión para entornos de producción.
