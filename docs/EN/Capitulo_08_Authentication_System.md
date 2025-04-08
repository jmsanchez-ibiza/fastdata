# Chapter 8 - Authentication System

The authentication system in FastApp is responsible for protecting sensitive application routes and ensuring that only valid users can access certain functionalities.

It is implemented through a combination of:

- Credential validation  
- Session generation and verification  
- Decorators to protect routes  

---

## 🔑 Login

The login form is defined in `src/views/login_views.py`.

---

## 🔍 Credential Verification

This is handled in `src/auth/login.py`. The logic searches for the user in the database and compares the username and password.  
Passwords are encrypted using `hash`.

> *Note: In a production application, the `password` column (unencrypted) should be removed, and only the `password_hash` column should be used.*

---

## 📦 Login Handler

In `src/controllers/login_controller.py`, the logic for the `/login`, `/logout`, and `/login_post` endpoints is defined, handling user login and credential verification.

---

## 🔐 Sessions

- Sessions are internally managed by `fasthtml`.  
- The `session` object allows the user's state to be persistently stored throughout navigation.

---

## 🚪 Logout

The route is defined in `login_controller.py` under `/logout`.  
This clears the user's session and redirects them to the home screen.

---

## 🛡️ Route Protection

FastApp uses several functions located in `src/auth/login.py` to block access to routes when a user is not logged in or if their role does not meet the required level.

---

## 🧪 Test Data

The script `__create_data.py` generates a user with the following credentials:
```
Email: admin@example.com
Password: admin
```

---

This simple but functional system covers the basic authentication requirements for an admin-style app.  
It can be easily enhanced with features like password hashing and session expiration for production environments.

---