#The Core SQLAlchemy Setup

#This file is where you establish the foundational component

# For creating the database engine and connection
from sqlalchemy import create_engine, text
# For defining database tables using ORM (if you plan to use ORM)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#Engine : Responsible for SQL alchemy to connect to a Postgres Database, engine is responsible for establishing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

#All of the model that we define to create our tables in Postgres will be extending this Base class
Base = declarative_base()

#Any Python class that represents a database table in SQLAlchemy's ORM must inherit from this Base class.

def get_db():               #To make that session
    db = SessionLocal()
    try:
        yield db
    finally:db.close()

