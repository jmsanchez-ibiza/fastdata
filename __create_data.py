import random

from src.data.database import Database
from src.data.table_DAO import TableDAO
from src.data.models import User
from faker import Faker

dbase = Database()
inspector = dbase.get_inspector()
tables_list = inspector.get_table_names()

respuesta = input("Are you sure you want to create the database and the initial data? (Y/N): ")
if respuesta.lower() == 's':
    random_number = random.randint(1000, 9999)
    respuesta_numero = int(input(f"Please enter the random number {random_number}: "))
    if respuesta_numero == random_number:
        dbase._init_db()
        print(f"Database ({dbase.database_uri}) creada.")
    else:
        print("Incorrect number. Operation canceled..")
else:
    print("Operation canceled.")

dbase = Database()

#  List of tables that will be created
to_be_created_list = [
    "users"
    "--end--"
]

# Create users
if "users" in to_be_created_list:
    
    try:
        USERS = [
            {"username": "yoss", "user_code": 1, "name": "Yoss Sanch", "email": "yoss@sanch.com", "password": "1234", "role": "admin", "active": "Y", "blocked": "N"},
            {"username": "user", "user_code": 2, "name": "General user", "email": "userbyexample@mail.com", "password": "1111", "role": "general", "active": "Y", "blocked": "N"},
        ]
        
        # Check if the table already exists, then ask if we want to create more data
        dao = TableDAO(User)
        table_name = User.__tablename__
        register_count = dao.get_count()
        if table_name in tables_list and register_count > 0:
            # La tabla existe y tiene registros
            input(f"La tabla {table_name} existe y tiene {register_count} registros.\nPulse una tecla para continuar...\no Ctrl-C para cancelar... ")

        for user in USERS:
            new_user = User()
            new_user.username = user["username"]
            new_user.user_code = int(user["user_code"])
            new_user.name = user["name"]
            new_user.email = user["email"]
            new_user.password = user["password"]
            new_user.password_hash = new_user.set_password(user["password"])
            new_user.role = user["role"]
            new_user.active = user["active"]
            new_user.blocked = user["blocked"]
            dao.create(new_user)

    except Exception as e:
        input(f"There was an error while creating the users.\n{e}\n\nPress any key to continue ...")

