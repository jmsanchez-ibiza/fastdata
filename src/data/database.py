from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import DATABASE_URI

Base = declarative_base()

engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import *

class Database:

    def __init__(self, database_uri = None):

        self.database_uri = database_uri or DATABASE_URI
        self.engine = create_engine(self.database_uri, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.inspector = inspect(self.engine)


    def _init_db(self):
        """Create the database tables according to the defined models"""
        try:
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print(f"ERROR: in _init_db() -> {e}")
            input("Press any key to continue ...")

    def get_inspector(self):
        return self.inspector



    @contextmanager
    def get_connection(self):
        engine = create_engine(self.database_uri, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        try:
            yield db

        finally:
            db.close()

# Singleton instance of the Database class to be used throughout the application
# This is a simple way to ensure that the same instance is used everywhere
dbase = Database()

