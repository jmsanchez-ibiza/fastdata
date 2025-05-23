import random

from src.data.database import Database
from src.data.DAO_users import UserDAO
from src.data.DAO_clients import ClientDAO
from src.data.models import User, Client
from faker import Faker

dbase = Database()
inspector = dbase.get_inspector()
tables_list = inspector.get_table_names()

response = input("Are you sure you want to create the database and the initial data? (Y/N): ")
if response.lower() == 'y':
    random_number = random.randint(1000, 9999)
    response_numero = int(input(f"Please enter the random number {random_number}: "))
    if response_numero == random_number:

        dbase._init_db()
        print(f"Database ({dbase.database_uri}) creada.")
    else:
        print("Incorrect number. Operation canceled..")
else:
    print("Operation canceled.")

dbase = Database()

#  List of tables that will be created
to_be_created_list = [
    "users",
    "clients",
    "--end--"
]

# Create users
if "users" in to_be_created_list:
    
    try:
        USERS = [
            {"username": "admin", "user_code": 1, "name": "Admin user", "email": "admin@mail.com", "password": "12345", "role": "admin", "active": "Y", "blocked": "N"},
            {"username": "user", "user_code": 2, "name": "General user", "email": "userbyexample@mail.com", "password": "11111", "role": "general", "active": "Y", "blocked": "N"},
        ]
        
        # Check if the table already exists, then ask if we want to create more data
        dao = UserDAO()
        table_name = User.__tablename__
        register_count = dao.get_count()
        if table_name in tables_list and register_count > 0:
            # The table exists and contains records.
            input(f"Table: {table_name} exists and contains {register_count} records.\nPress any key to continue...\nor Ctrl-C to cancel... ")

        for i, user in enumerate(USERS):
            new_user = User()
            new_user.id = i + 1
            new_user.username = user["username"]
            new_user.user_code = int(user["user_code"])
            new_user.name = user["name"]
            new_user.email = user["email"]
            new_user.password = new_user.password_hash = user["password"]
            new_user.set_password(user["password"])
            print("-"*30, new_user.password, new_user.password_hash)
            new_user.role = user["role"]
            new_user.active = user["active"]
            new_user.blocked = user["blocked"]
            last_id, error = dao.create(new_user)
            print(f"{last_id=}, {error=}, {new_user=}")

        print("<User> processed Table.")

    except Exception as e:
        input(f"There was an error while creating the users.\n{e}\n\nPress any key to continue ...")

# Create clients
es_fake = Faker("es_ES")
fake = Faker("en_US")
Faker.seed(0)
if "clients" in to_be_created_list:
    try:
        dao = ClientDAO()
        for i in range(100):
            c = Client()
            name = str(fake.name())
            c.clcomer = c.clname = name.upper()
            c.dni_nie_cif = es_fake.nif()
            c.email_payment = fake.email()
            c.country = fake.country()
            c.language = fake.language_code()
            c.payment_method = random.choice(["01", "02", "03"])
            dao.create(c)
            print(c)
        print("<Client> processed Table.")

    except Exception as e:
        input(f"ERROR creating Client's table.\n{e}")
        input("Press any key to continue ...")
