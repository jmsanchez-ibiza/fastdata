# Chapter 12 - Testing and Data Generation

FastApp includes a simple yet functional mechanism to populate the database with test data. This makes it easier to verify system behavior, run demos, and develop without needing to manually input data through the interface.

---

## 🧪 Test Data Script

The `__create_data.py` file is responsible for creating:

- The necessary database tables  
- A set of sample users, clients, and contacts  

---

## 🧰 How to Use It

Simply run:

```bash
python __create_data.py
```

This will:
- Clear any previous content (if configured to do so)  
- Populate the `fastdata.db` database with records ready for testing  

---

## 🎯 Purpose

- Ideal for live demos  
- Useful when starting the project for the first time  
- Helps test forms, modals, and tables  

---

## 🛡️ Considerations

- This script is intended for development environments  
- It should not be run in production without modifications  
- It can be extended to generate fixtures or random test data  

---

In summary, `__create_data.py` is a helpful tool for speeding up the development cycle and ensuring that the app always has data available to work with instantly.

---