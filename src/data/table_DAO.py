from typing import Any, Dict, Tuple, Optional, Type, List, Union
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from .database import dbase
from .models import BaseModel

class TableDAO:
    """Base class for DAOs (Data Access Objects) that handle CRUD operations in the database."""

    def __init__(self, model: Type[BaseModel]):
        self.model = model

    def create(self, entity: BaseModel) -> Tuple[int, Optional[Exception]]:
        """
        Create a new record from a model object.
        
        Args:
            entity: BaseModel - Model object with the data for the new record.
        
        Retorna:
            Tuple[int, Optional[Exception]]: ID of the new record or 0 if there was an error, and the error (if any).
        """
        try:
            with dbase.get_connection() as db:
                db.add(entity)
                db.commit()
                return entity.id, None
        except Exception as e:
            return 0, e

    def update(self, entity: BaseModel) -> Tuple[int, Optional[Exception]]:
        """
        Update an existing record.

        Args:  
            entity: BaseModel - The model object with the updated data.

        Returns:  
            Tuple[int, Optional[Exception]]: ID of the updated record or 0 if there was an error, and the error (if any).
        """
        try:
            with dbase.get_connection() as db:
                merged_entity = db.merge(entity)
                db.commit()
                return merged_entity.id, None
        except Exception as e:
            return 0, e

    def delete(self, entity_id: int) -> Tuple[int, Optional[Exception]]:
        """
        Delete a record by its ID.

        Args:  
            entity_id: integer - The ID of the record to delete.

        Returns:  
            Tuple[int, Optional[Exception]]: ID of the deleted record or 0 if there was an error, and the error (if any).
        """
        try:
            with dbase.get_connection() as db:
                entity = db.query(self.model).filter_by(id=entity_id).first()
                if entity:
                    db.delete(entity)
                    db.commit()
                    return entity.id, None
                else:
                    return 0, f"No se encontró el registro: {entity_id}"
        except Exception as e:
            return 0, e

    def get_all(
        self,
        load_relationships: bool = True,
        filter: Union[Dict[str, Any], None] = None,
        order_by: Union[Dict[str, str], None] = None
    ) -> List[BaseModel]:
        """
        Retrieve a list of all records.

        Args:  
            load_relationships: bool -  Whether to load relationships (default is True).  
            filter: Dict[str, Any] -    Dictionary with filtering conditions (optional).  
            order_by: Dict[str, str] -  Dictionary with columns and sorting directions (optional).  
                                        Example: {"name": "ASC", "creation_date": "DESC"}
        Returns:  
            List[BaseModel]: List of records.
        """
        with dbase.get_connection() as db:
            query = db.query(self.model)
            
            # Apply filter if provided
            if filter:
                query = query.filter_by(**filter)
            
            # Load relationships if requested
            if load_relationships:
                query = query.options(joinedload("*"))
            
            # Apply sorting if provided
            if order_by:
                for columna, direccion in order_by.items():
                    if direccion.upper() == "ASC":
                        query = query.order_by(asc(columna))
                    elif direccion.upper() == "DESC":
                        query = query.order_by(desc(columna))
                    else:
                        raise ValueError(f"Invalid sorting direction: {direccion}. Use 'ASC' or 'DESC'.")
            
            return query.all()

    def get_by_id(self, entity_id: int, cargar_relaciones: bool = False) -> Optional[BaseModel]:
        """
        Retrieve a record by its ID.

        Args:  
            entity_id: int -            The ID of the record we are looking for.  
            load_relationships: bool -  Whether to load relationships (default is False).

        Returns:  
            Optional[BaseModel]: The record or None if not found.
        """
        with dbase.get_connection() as db:
            if cargar_relaciones:
                return db.query(self.model).options(joinedload("*")).filter_by(id=entity_id).first()
            else:
                return db.query(self.model).filter_by(id=entity_id).first()
    
    def get_count(self):
        with dbase.get_connection() as db:
            return db.query(self.model).count()