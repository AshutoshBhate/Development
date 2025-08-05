#Special file that pytest uses. Allows us to define fixtures

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.main_Routers import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

#Engine : Responsible for SQL alchemy to connect to a Postgres Database, engine is responsible for establishing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

Base.metadata.create_all(bind=engine)    #This will create all of out tables

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': 'ashutoshbhate@gmail.com', 'password': "password123"}
    
    response = client.post("/users/", json = user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    
    return new_user