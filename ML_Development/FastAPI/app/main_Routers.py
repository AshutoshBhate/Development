from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth
from pydantic_settings import BaseSettings
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)    #This will create all of out tables

app = FastAPI()

origins= ["https://www.google.com", "https://www.youtube.com"]
#origins= ["*"] Allow request from every single domain

app.add_middleware(     #Middleware is a function that runs before every request
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True, # Set to True if you need to send cookies or authorization headers
    allow_methods=["*"],    # Allows all standard methods (GET, POST, PUT, DELETE, OPTIONS, etc.) / But without *, it allows only certain HTTP methods
    allow_headers=["*"],    # Allows all headers
)

@app.get("/")
def hello():
    return {"message": "Hello World"}
    
#Connecting to Database : Redundant here, the actual connection is done my engine, Session, etc. of database.py
# while True:    
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user = 'postgres', 
#                                 password = 'galvatron', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection was successful!")
#         break
#     except Exception as error:
#         print("Connection to Database failed")
#         print("Error was : ", error)
#         time.sleep(2)
        
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)