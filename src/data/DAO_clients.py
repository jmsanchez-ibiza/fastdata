from .models import Cliente
from .table_DAO import TableDAO

class ClienteDAO(TableDAO):
    def __init__(self):
        super().__init__(Cliente)