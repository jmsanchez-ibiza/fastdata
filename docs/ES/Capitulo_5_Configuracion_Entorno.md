# Capítulo 5 - Configuración y Entorno

La correcta configuración del entorno es esencial para ejecutar FastApp en modo local o producción. Este capítulo explica los requisitos del sistema, las variables de entorno utilizadas y cómo preparar todo para el desarrollo.

---

## 📦 Requisitos del Sistema

- **Python**: 3.12 o superior
- **Gestor de paquetes**: `pip`
- **SQLite**: Base de datos por defecto
- **Dependencias**: especificadas en `requirements.txt` (opcionalmente generable con `pip freeze`)

---

## 🧪 Instalación del Entorno de Desarrollo

1. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Opcional) Crear base de datos de prueba**:
   Ejecutar el script `__create_data.py` para poblar la base de datos con usuarios, clientes y contactos:

   ```bash
   python __create_data.py
   ```

---

## 🔐 Variables de Entorno

FastApp utiliza un archivo `.env` en la raíz del proyecto para definir variables sensibles:

### Ejemplo de `.env`:
```env
SECRET_KEY=clave_super_secreta
DEBUG=True
DATABASE_URL=sqlite:///fastdata.db
```

### Uso en el código:
Archivo `src/config.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

Este enfoque:
- Evita exponer datos sensibles en el código.
- Permite cambiar de base de datos sin alterar código fuente.
- Mejora la seguridad en entornos de producción.

---

## 🧩 Integración de Base de Datos

La conexión con SQLite está definida en `src/data/database.py`:

Se crea una variable `dbase` (Singleton) que es accesible desde cualquier parte del código de la aplicación.
También se usan DAOs (Data Access Objects), para hacer más fácil y encapsulado el acceso a los datos.

Gracias a SQLAlchemy, la gestión de los datos de esta app pes muy fácilmente escalable y adaptable a PostgreSQL o MySQL simplemente cambiando la URL en `.env`:

```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

---

## 🛠️ Otros ajustes importantes

- Archivos de configuración como `.gitignore` evitan subir a Git archivos como `.env`, `.db` o `.pyc`.


---

## ✅ Verificación del entorno

Antes de ejecutar la aplicación:

- Asegúrate de tener la base de datos creada.
- Asegúrate de que el archivo `.env` esté configurado correctamente.
- Ejecuta `main.py` y verifica acceso a la ruta raíz ("/").

---

Este entorno flexible y bien estructurado permite ejecutar FastApp en distintas plataformas con mínimos cambios.
