# 🚀 fastdata

**fastdata** is a lightweight, modular data management web application built with **fasthtml**, **SQLAlchemy**, and **Bootstrap**. It demonstrates how to create dynamic and responsive interfaces entirely from Python—without relying on traditional frontend frameworks.

---

## 🛠️ Features

- 🔐 User authentication with session management  
- 🧑‍💼 CRUD operations for users, clients, and contacts  
- 📦 Modular MVC architecture  
- 🪟 HTMX-based modals for inline editing  
- 📤 Export data to Excel (`.xlsx`)  
- ⚡ Dynamic frontend with HTMX — no need for full-page reloads  
- 🎨 Custom styling with Bootstrap and CSS

---

## 📦 Installation

Make sure you are using **Python 3.12+**.

### Install core dependencies:

```bash
pip install python-dotenv python-fasthtml bcrypt sqlalchemy openpyxl
```

### (Optional) For generating sample data:

```bash
pip install faker
```

---

## 📚 About the Project

fastdata was created to showcase the capabilities of [fasthtml](https://github.com/AnswerDotAI/fasthtml), a Pythonic library for building declarative HTML UIs. It’s ideal for developers who want to build admin panels or CRUD apps without touching JavaScript-heavy frameworks.

---

## 📁 Project Structure

```
fastdata/
├── src/
│   ├── auth/           # Authentication logic
│   ├── controllers/    # Route handlers
│   ├── views/          # HTML views with fasthtml
│   ├── data/           # SQLAlchemy models and DAOs
│   ├── utils/          # Excel export, JS helpers
│   └── core/           # HTML wrappers and layout logic
├── static/             # CSS, JS, images
├── .env                # Environment variables
├── main.py             # Entry point
└── fastdata.db         # SQLite database
```

---

## 🧪 Development Utilities

Use the following command to generate sample users, clients, and contacts:

```bash
python __create_data.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

Built with:

- [fasthtml](https://github.com/AnswerDotAI/fasthtml)
- [HTMX](https://htmx.org)
- [Bootstrap](https://getbootstrap.com)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [OpenPyXL](https://openpyxl.readthedocs.io)

