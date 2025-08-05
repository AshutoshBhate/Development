#All the path operations dealing with users

from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix= "/users",
    tags= ["Users"] 
)


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse)
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

@router.get("/{id}", response_model = schemas.UserCreateResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    
    return user