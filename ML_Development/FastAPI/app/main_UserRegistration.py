from optparse import Option
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user


models.Base.metadata.create_all(bind=engine)    #This will create all of out tables

app = FastAPI()
    
#Connecting to Database
while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user = 'postgres', 
                                password = 'galvatron', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful!")
        break
    except Exception as error:
        print("Connection to Database failed")
        print("Error was : ", error)
        time.sleep(2)
        
@app.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Hash the password - user.password
    hashed_passowrd = utils.hash(user.password)     #We reference the password context
    user.password = hashed_passowrd
    
    
    new_user = models.User(**user.model_dump())     #This is where it knows which table to manipulate
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    #Here new_post is a SQLalchemy model 
    
    return new_user


#Set up a Route to a path operation that allows you to fetch and retrieve information about a user based of off their id
#Reasons: It can be a part of the authentication process

@app.get("/{id}", response_model = schemas.UserCreateResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    
    return user