# Capítulo 14 - Instrucciones para Ejecutar la App

Sigue estos pasos para clonar, configurar y ejecutar FastApp localmente en tu entorno de desarrollo.

---

## 📥 1. Clonar el Repositorio

```bash
git clone https://github.com/usuario/fastapp.git
cd fastapp
```

---

## 🧪 2. Crear un Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

---

## 📦 3. Instalar las Dependencias

```bash
pip install -r requirements.txt
```

Si no existe el archivo `requirements.txt`, puedes generarlo con:

```bash
pip freeze > requirements.txt
```

---

## ⚙️ 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con contenido como:

```env
SECRET_KEY=mi_clave_super_secreta
DATABASE_URL=sqlite:///fastdata.db
DEBUG=True
```

---

## 🧰 5. Crear la Base de Datos (Opcional)

```bash
python __create_data.py
```

Esto generará `fastdata.db` con datos de prueba.

---

## 🚀 6. Ejecutar la Aplicación

```bash
python main.py
```

Abre el navegador en `http://localhost:8000`.

---

## ✅ 7. Acceso de Prueba

Puedes iniciar sesión con:

- **Email**: admin@example.com
- **Contraseña**: admin

---

Una vez dentro, tendrás acceso completo al panel de usuarios, clientes y contactos.
