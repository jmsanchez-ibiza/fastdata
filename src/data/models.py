from fasthtml.common import add_toast
import bcrypt
from sqlalchemy import event, Column, Integer, String, Enum, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from .validators import validate_email, validate_nie_dni_cif
from .database import Base

# My Model Base class
# ===================================================================================
class BaseModel(Base):
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    # Common columns for all models
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String(50))
    updated_by = Column(String(50))


    def to_dict(self):
        """Converts the model instance into a dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Events to automatically update the created and updated fields
# ===================================================================================
@event.listens_for(BaseModel, 'before_insert')
def set_created_updated_on_insert(mapper, connection, target):
    target.created = datetime.now()
    target.updated = datetime.now()

@event.listens_for(BaseModel, 'before_update')
def set_updated_on_update(mapper, connection, target):
    target.updated = datetime.now()



# USER model
# ===================================================================================
class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column( Integer, primary_key=True, index=True )
    username = Column( String(45), unique=True, nullable=False )
    user_code = Column( Integer, unique=True, nullable=False )
    name = Column( String(80), nullable=False )
    email = Column( String(80), nullable=False )
    password = Column( String(25), nullable=False )
    password_hash = Column( String(200), nullable=False )
    role = Column( String(15), primary_key=False, unique=False, nullable=False, default="general" )

    active = Column( String(1), nullable=False, insert_default="y" )
    blocked = Column( String(1), nullable=False, default="n" )
    last_login = Column( DateTime, index=False, unique=False, nullable=True, default=None )
    
    address = Column( String(240), nullable=True, default="" )
    phone = Column( String(20), nullable=True, default="" )
    nif = Column( String(12), nullable=True, default="" )
    nns = Column( String(15), nullable=True, default="" )
    notes = Column(Text, nullable=True, default="")

    @property
    def is_admin(self):
        """ Check if the user is an administrator """
        return self.role.lower() == "admain"
    
    def in_role(self, gtest: str =""):
        """ Check if the user belongs to the role 'gTest' """
        return gtest.lower() in self.role.lower()

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
    
    def validate_data(self, accion, session) -> dict:
        """Validar el registro según la acción (add o edit)"""
        errors = {}
        if not self.user_code: errors['user_code'] = "Enter a unique user code.."
        if len(self.username) < 3: errors['username'] = "The <username> must be at least 3 characters long."
        if len(self.name) < 3: errors['name'] = "The name must be at least 3 characters long."
        # TODO: Validate that the password is correct (e.g., one uppercase, one lowercase, 3 digits...).
        if not self.password: errors['password'] = "Enter a password."
        if not self.role: errors['role'] = "Select a role for the user."
        if self.email and not validate_email(self.email): errors['email'] = "This is nota a valid email."

        # TODO: User handling, to be global and automatically updated in before_insert or before_update  
        # so the following code can be removed
        
        # FORMAT: session['user'] =  {"username":"admin", "password": "1234", "role": "admin"}
        if accion=="edit":
            self.updated_by = session['user']['username'] if 'user' in session else ""
        if accion=="add":
            self.created_by = self.updated_by = session['user']['username'] if 'user' in session else ""

        return errors
    

    def set_password(self, password: str) -> bytes:
        # Generate a salt and encrypt the password.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = hashed_password
    

    def check_password(self, password: str) -> bool:
        # Verificar si la contraseña coincide con el hash almacenado
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
   
# CLIENTs model
# ===================================================================================
class Client(BaseModel):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    clcomer = Column(String(100), nullable=False, index=True)
    clname = Column(String(100), nullable=False, index=True)
    dni_nie_cif = Column(String(15), nullable=False)
    email_heading = Column(String(100))
    email_payment = Column(String(100), default=False)
    email_payment_cc = Column(Text)
    adress = Column(String(150))
    cp = Column(String(10))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(2), nullable=False, default="ES")
    language = Column(String(2), nullable=False, default="00")
    payment_method = Column(String(2), nullable=False, default="01")
    payment_responsible = Column(String(50))
    notes = Column(Text)
    # Relations
    contacts = relationship("Contact", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Client {self.id} : {self.clcomer} - {self.clname}->{self.dni_nie_cif}>'

    @property
    def can_delete(self):
        return len(self.contacts) == 0

    def validate(self, accion, session):
        """Validate the record according to the action (add or edit)"""
        errors = {}
        if len(self.clcomer) < 3: errors['clcomer'] = "The trade name must have at least 3 characters"
        if len(self.clname) < 3: errors['clname'] = "The invoicing name must have at least 3 characters"
        if not validate_nie_dni_cif(self.dni_nie_cif): errors["dni_nie_cif"] = "Invalid identification Dni/Nie/Cif"
        if self.email_de_cobro and not validate_email(self.email_de_cobro): errors['email_de_cobro'] = "Invalid email address"
        if self.email_de_cobro_cc and not validate_email(self.email_de_cobro_cc): errors['email_de_cobro_cc'] = "Invalid email address"


        # TODO: User handling, to be global and automatically updated in before_insert or before_update  
        # so the following code can be removed
        # FORMAT: session['user'] =  {"username":"admin", "password": "1234", "role": "admin"}
        if accion=="edit":
            self.updated_by = session['user']['username'] if 'user' in session else ""
        if accion=="add":
            self.created_by = self.updated_by = session['user']['username'] if 'user' in session else ""

        return errors

    @property
    def can_delete(self):
        # Can be deleted if no associated contacts exist
        return len(self.contactos) == 0

class Contact(BaseModel):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(Integer, ForeignKey('clients.id', ondelete="RESTRICT"))
    contact_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    mobile = Column(String(20))
    email = Column(String(100))
    notes = Column(Text)
    created = Column(DateTime)
    created_by = Column(String(50))
    updated = Column(DateTime)
    updated_by = Column(String(50))

    client = relationship("Client", back_populates="contacts")

    def __repr__(self):
        return f'<Client {self.id_cliente} : {self.id} - {self.contact_name}->{self.client.clcomer}>'

    def validate(self, accion, session):
        """Validate the record according to the action (add or edit)"""

        errors = {}
        if len(self.contact_name) < 3: errors['contact_name'] = "The contact name must have at least 3 characters"
        if self.email and not validate_email(self.email): errors['email'] = "Invalid email"

        # TODO: User handling, to be global and automatically updated in before_insert or before_update  
        # so the following code can be removed
        # FORMAT: session['user'] =  {"username":"admin", "password": "1234", "role": "admin"}
        if accion=="edit":
            self.updated_by = session['user']['username'] if 'user' in session else ""
        if accion=="add":
            self.created_by = self.updated_by = session['user']['username'] if 'user' in session else ""

        return errors
