from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags= ['Authentication'])

# @router.post('/login')
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Invalid Credentials")
    
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Invalid Credentials")
    
#     #Create a Token
#     #Return Token
#     #return {"token": "Example Token"}
    
#     access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
#     return {"access_token": access_token, "token_type": "bearer"}



@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #This above will return
    # {
    #     "username": "blah",
    #     "password": "another"
    # }
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  
    
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")  
    
    #Create a Token
    #Return Token
    #return {"token": "Example Token"}  
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})  
    
    return {"access_token": access_token, "token_type": "bearer"}


#NOW THE LOGIC TO SEE WHETHER THE TOKEN HAS NOT BEEN TAMPERED WITH AND HAS NOT EXPIRED
