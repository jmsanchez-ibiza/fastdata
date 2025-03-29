from typing import Optional
from .models import User
from .table_DAO import TableDAO
from .database import dbase

class UserDAO(TableDAO):
    """DAO for the user model"""
    def __init__(self):
        super().__init__(User)


    # Specific functions for this model
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their USERNAME.

        Args:  
            username: str - USERNAME of the user we are looking for.

        Returns:  
            Optional[User]: The user or None if not found.
        """
        with dbase.get_connection() as db:
            return db.query(self.model).filter_by(username=username).first()