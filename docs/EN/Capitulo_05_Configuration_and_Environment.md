# Chapter 5 - Configuration and Environment

Proper environment setup is essential to run FastApp in either local or production mode. This chapter explains the system requirements, environment variables used, and how to prepare everything for development.

---

## 📦 System Requirements

- **Python**: 3.12 or higher  
- **Package manager**: `pip`  
- **SQLite**: Default database  
- **Dependencies**: specified in `requirements.txt` (optionally generated with `pip freeze`)

---

## 🧪 Setting Up the Development Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Create a test database**:
   Run the script `__create_data.py` to populate the database with sample users, clients, and contacts:

   ```bash
   python __create_data.py
   ```

---

## 🔐 Environment Variables

FastApp uses a `.env` file at the project root to define sensitive variables:

### Example `.env`:
```env
SECRET_KEY=super_secret_key
DEBUG=True
DATABASE_URL=sqlite:///fastdata.db
```

### Usage in the code:  
In the file `src/config.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

This approach:
- Prevents exposing sensitive data in the code.
- Allows switching databases without changing source code.
- Enhances security in production environments.

---

## 🧩 Database Integration

The connection to SQLite is defined in `src/data/database.py`:

A `dbase` variable (Singleton) is created and can be accessed from anywhere in the application.  
DAOs (Data Access Objects) are also used to simplify and encapsulate data access.

Thanks to SQLAlchemy, data management in this app is easily scalable and adaptable to PostgreSQL or MySQL by simply changing the URL in `.env`:

```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

---

## 🛠️ Other Important Settings

- Configuration files like `.gitignore` prevent uploading files such as `.env`, `.db`, or `.pyc` to Git.

---

## ✅ Environment Check Before Running

Before running the application:

- Make sure the database is created.
- Ensure the `.env` file is properly configured.
- Run `main.py` and verify access to the root route ("/").

---

This flexible and well-structured environment allows FastApp to run across various platforms with minimal changes.

---