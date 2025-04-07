# Capítulo 8 - Sistema de Autenticación

El sistema de autenticación en FastApp se encarga de proteger las rutas sensibles de la aplicación y garantizar que sólo usuarios válidos puedan acceder a ciertas funcionalidades.

Está implementado mediante una combinación de:

- Validación de credenciales
- Generación y verificación de sesiones
- Decoradores para proteger rutas

---

## 🔑 Inicio de Sesión

El formulario de login se encuentra definido en `src/views/login_views.py`:

```python
def login_form():
    with Form("/login", method="post"):
        Input(_name="email", _type="email", _placeholder="Correo", _class="form-control")
        Input(_name="password", _type="password", _placeholder="Contraseña", _class="form-control")
        Button("Iniciar sesión", _type="submit", _class="btn btn-primary")
```

---

## 🔍 Verificación de Credenciales

Se gestiona en `src/auth/login.py`. Esta lógica busca el usuario en la base de datos y compara la contraseña:

```python
def check_credentials(email, password):
    with Session() as session:
        user = session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            return user
```

> *Nota: en una aplicación real, la contraseña debería estar cifrada con `bcrypt` o similar.*

---

## 📦 Manejador de Login

En `src/controllers/login_controller.py` se define la lógica del endpoint `/login`:

```python
@route("/login", method="POST")
def do_login(ctx):
    form = ctx.form()
    user = check_credentials(form["email"], form["password"])
    if user:
        ctx.session["user_id"] = user.id
        return Redirect("/")
    else:
        return login_views.login_form(error="Credenciales incorrectas")
```

---

## 🔐 Sesiones

- Las sesiones están gestionadas internamente por `fasthtml`.
- El `ctx.session` permite almacenar el estado del usuario de forma persistente durante su navegación.

---

## 🚪 Cierre de Sesión

Ruta definida en `login_controller.py`:
```python
@route("/logout")
def logout(ctx):
    ctx.session.clear()
    return Redirect("/login")
```

Esto borra toda la sesión del usuario y lo redirige a la pantalla de login.

---

## 🛡️ Protección de Rutas

FastApp utiliza un decorador personalizado `@authenticated` para bloquear rutas si el usuario no está logueado.

Ejemplo:
```python
@route("/users")
@authenticated
def index(ctx):
    ...
```

Este decorador:
- Verifica si `ctx.session["user_id"]` existe.
- Si no existe, redirige a la página de login.

---

## 🧪 Datos de Prueba

El script `__create_data.py` genera un usuario con el email y contraseña:
```
Email: admin@example.com
Password: admin
```

---

Este sistema simple pero funcional cubre los requisitos básicos de autenticación para una app administrativa. Puede mejorarse fácilmente con cifrado de contraseñas y expiración de sesión para entornos de producción.
