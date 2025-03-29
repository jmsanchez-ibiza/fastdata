from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import create_engine, event, Column, Integer, String, Enum, Text, DateTime, Boolean, ForeignKey, Float
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
        # self.Base = declarative_base()


    def _init_db(self):
        """Crear las tablas de la base de datos según los modelos definidos"""
        try:
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print(f"ERROR: en _init_db() -> {e}")
            input("Pulse una tecla para continuar ...")

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

# Instancia singleton
dbase = Database()

