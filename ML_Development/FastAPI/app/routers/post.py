#All our path operations dealing with posts

from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db
from typing import List, Optional

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

#GET (ALL POSTS)

# This is for returning how many a particular email has how many posts
# @router.get("/user", response_model= List[schemas.UserWithPostCountResponse])   #We have to import something to specify a list of posts

@router.get("/user", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int=  Depends(oauth2.get_current_user), 
              limit: int= 10, skip: int= 0, search: Optional[str]= ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # If you want to return only you posts (Only the posts of the logged in user) 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # query_results = db.query(models.User, func.count(models.Post.owner_id).label("Post Count")).join(models.Post, models.User.id == models.Post.owner_id, isouter= True).group_by(models.User.id).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()   #By default, it is a left inner join, we need to set this as an outer
    # formatted_results = []
    
    # for user_obj, post_count_val in query_results:
    #     formatted_results.append(schemas.UserWithPostCountResponse(id = user_obj.id,
    #                                                                email = user_obj.email,
    #                                                                post_count = post_count_val))
    
    # return formatted_results
    
    return posts

#GET (SPECIFIC ID)

# @router.get("/{id}", response_model= schemas.PostResponse)
# def get_posts(id: int, db: Session = Depends(get_db), user_id: int=  Depends(oauth2.get_current_user)):
#     test_post = db.query(models.Post).filter(models.Post.id == id).first()
#     print(test_post.content)
    
#     if not test_post:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id : {id} was not found")
#     return test_post

#We are now trying to see if the get_current_user can work with ids

@router.get("/{id}", response_model= schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db), current_user: models.User=  Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    print(post.content)
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} was not found")
        
    # If you want to return only you posts (Only the posts of the logged in user)    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    return post

#POST

# @router.post("/", status_code= status.HTTP_201_CREATED)
# def create_post(post: CreatePost, db: Session = Depends(get_db)):
#     new_post = models.Post(title = post.title, content = post.content, published = post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"data": new_post}

#POST (UNPACKING THE DICTIONARY)
#If we add new fields in models.Post, this method automatically unpack it for us and we don't need to always do post.title, post.content, etc.

# @router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
# def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), user_id: int=  Depends(oauth2.get_current_user)):
    
#     print(user_id)
#     new_post = models.Post(**post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)    #Here new_post is a SQLalchemy model 
    
#     #pydantic only knows how to work with dictionaries
    
#     return new_post

#We are now trying to see if the get_current_user can work with ids

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User= Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    #Here new_post is a SQLalchemy model 
    
    #pydantic only knows how to work with dictionaries
    
    return new_post

#DELETE

# @router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db), user_id: int=  Depends(oauth2.get_current_user)):
    
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     print(post_query)
    
#     if post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     post_query.delete(synchronize_session= False)
#     db.commit()
    
#     return Response(status_code= status.HTTP_204_NO_CONTENT)

#We are now trying to see if the get_current_user can work with ids

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User=  Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post_query)
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
        
    
    post_query.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)

#UPDATE

# @router.put("/{id}", response_model= schemas.PostResponse)
# def update_post(id: int, another_post: schemas.UpdatePost, db: Session = Depends(get_db), user_id: int=  Depends(oauth2.get_current_user)):
    
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
    
#     if post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     post_query.update(another_post.model_dump(), synchronize_session= False)
#     db.commit()
    
#     return post_query.first()

#We are now trying to see if the get_current_user can work with ids

@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, another_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: models.User=  Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    post_query.update(another_post.model_dump(), synchronize_session= False)
    db.commit()
    
    return post_query.first()

