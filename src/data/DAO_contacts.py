from typing import Optional
from .models import Contact
from .table_DAO import TableDAO
from .database import dbase

class ContactDAO(TableDAO):
    def __init__(self):
        super().__init__(Contact)

    # Specific functions for this model
    def get_all_by_client_id(self, cliente_id: int) -> Optional[Contact]:
        """
        Retrieve all contacts for a client.

        Args:  
            user_id: int - ID of the client we are looking for.

        Returns:  
            Optional[Contact]: The contacts found.
        """
        with dbase.get_connection() as db:
            return db.query(self.model).filter_by(id_client=cliente_id).order_by(Contact.contact_name).all()

