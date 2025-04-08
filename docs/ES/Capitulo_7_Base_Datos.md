# Capítulo 7 - Base de Datos

FastApp utiliza **SQLite** como motor de base de datos por defecto, lo cual permite una configuración rápida y sin dependencias externas. Sin embargo, gracias al uso de **SQLAlchemy**, el sistema es fácilmente escalable a otros motores como **PostgreSQL**, **MySQL** o **MariaDB** con sólo modificar la cadena de conexión en el archivo `.env`.

---

## 🧱 ORM con SQLAlchemy

El modelo de datos está definido en el archivo `src/data/models.py`. Aquí se emplea SQLAlchemy para representar las tablas como clases de Python.

### Ejemplo:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    ...
```

Este modelo representa una tabla `users` con las columnas `id`, `name` y `email`.

---

## 🔌 Conexión a la Base de Datos

Definida en `src/data/database.py` se usa la clase Database y finalmente se declara:
```python
dbase = Database()
```
Una instancia Singleton de la clase Database que puede ser usada en toda la aplicación.

Este código permite:
- Conectar a SQLite en desarrollo.
- Cambiar fácilmente a otra base de datos solo editando la variable `DATABASE_URL` en el archivo `.env`.

---

## 🧩 DAOs (Data Access Objects)

Cada entidad tiene su propia clase DAO para manejar las operaciones CRUD.

Ejemplo en `DAO_users.py`:
```python
class UserDAO(TableDAO):
    """DAO for the user model"""
    def __init__(self):
        super().__init__(User)


    # Specific functions for this model
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their USERNAME.

        Args:  
            username: str - USERNAME of the user we are looking for.

        Returns:  
            Optional[User]: The user or None if not found.
        """
        with dbase.get_connection() as db:
            return db.query(self.model).filter_by(username=username).first()
    
    ...
```

Ventajas del enfoque DAO:
- Uso de la clase base `TableDAO`, para la mayoría de las acciones necearias
- Uso de cada clase para cada modelo como `UserDAO`, dónde se heredan las funciones 
  de `TableDAO` y se definen funciones específicas de cada modelo como en este
  caso `get_user_by_username()`.
- Separación clara entre lógica de negocio y acceso a datos.
- Reutilización de código.
- Mejora la testabilidad.

---

## 🧪 Validación de Datos

El archivo `validators.py` define funciones para comprobar campos antes de insertar o actualizar registros.

Ejemplo: `validate_email(email)`, para validar campos con los formatos correctos de email.

Estas funciones son utilizadas en los controladores antes de actualizar o insertar registros.

---

## 🔄 Creación y Reset de Datos

Para generar una base de datos inicial, se incluye el script `__create_data.py`.

Este archivo:
- Crea las tablas con `Base.metadata.create_all(engine)`.
- Inserta datos de ejemplo (usuarios, clientes, contactos).
- Es útil para pruebas o demostraciones.

---

## 📈 Esquema Relacional Simplificado

- `users`: Usuarios del sistema
- `clients`: Clientes gestionados
- `contacts`: Contactos asociados a cada cliente (relación 1:N)

```text
users
 └── id (PK)

clients
 └── id (PK)

contacts
 └── id (PK)
 └── client_id (FK → clients.id)
```

---

## 🔐 Seguridad y Persistencia

- El archivo de base de datos (`fastdata.db`) se crea en la raíz.
- Las sesiones están protegidas por tokens y claves en `.env`.

---

Este sistema de base de datos modular y portable permite escalar el proyecto a entornos productivos sin cambiar el código, sólo modificando la configuración.
