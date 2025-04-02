from .models import Client
from .table_DAO import TableDAO

class ClientDAO(TableDAO):
    def __init__(self):
        super().__init__(Client)