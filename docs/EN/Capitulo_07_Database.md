# Chapter 7 - Database

FastApp uses **SQLite** as its default database engine, allowing for quick setup without external dependencies. However, thanks to **SQLAlchemy**, the system is easily scalable to other engines like **PostgreSQL**, **MySQL**, or **MariaDB** by simply modifying the connection string in the `.env` file.

---

## 🧱 ORM with SQLAlchemy

The data model is defined in the file `src/data/models.py`. Here, SQLAlchemy is used to represent tables as Python classes.

### Example:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    ...
```

This model represents a `users` table with the columns `id`, `name`, and `email`.

---

## 🔌 Database Connection

Defined in `src/data/database.py`, the `Database` class is used and instantiated as follows:
```python
dbase = Database()
```
A singleton instance of the `Database` class that can be used throughout the application.

This setup allows:
- Connecting to SQLite during development.
- Easily switching to another database by editing the `DATABASE_URL` in the `.env` file.

---

## 🧩 DAOs (Data Access Objects)

Each entity has its own DAO class to handle CRUD operations.

Example from `DAO_users.py`:
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
```

Advantages of the DAO approach:
- Use of the base class `TableDAO` for most common actions.
- Each model has its own class like `UserDAO`, inheriting from `TableDAO` and defining specific functions like `get_user_by_username()`.
- Clear separation between business logic and data access.
- Code reuse.
- Easier to test.

---

## 🧪 Data Validation

The `validators.py` file defines functions to validate fields before inserting or updating records.

Example: `validate_email(email)` checks whether the email format is correct.

These functions are used in the controllers before inserting or updating records.

---

## 🔄 Data Creation and Reset

To generate an initial database, the script `__create_data.py` is included.

This file:
- Creates the tables using `Base.metadata.create_all(engine)`.
- Inserts sample data (users, clients, contacts).
- Is useful for testing or demos.

---

## 📈 Simplified Relational Schema

- `users`: System users  
- `clients`: Managed clients  
- `contacts`: Contacts associated with each client (1:N relationship)

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

## 🔐 Security and Persistence

- The database file (`fastdata.db`) is created at the project root.
- Sessions are protected by tokens and keys defined in `.env`.

---

This modular and portable database system allows the project to scale to production environments without changing the code—only the configuration.

---