from optparse import Option
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . import schemas
from .routers import post

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
    
my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, 
            {"title" : "favourite foods", "content" : "I like pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i    #Will give us the index of that id
        
############################################## SQLALCHEMY #############################################################

#INITIAL TRIAL
      
# @app.get("/sqlalchemy")                         #The 'posts' table pops up in tables section, all column names come from models.py
# def test_posts(db: Session = Depends(get_db)):  #get_db creates a Session for every request
#     return {"status": "Success"}

#TO RETRIEVE ALL THE ROWS OF THE DATABASE

# @app.get("/sqlalchemy")                             #Path Operation Decorator              
# def test_posts(db: Session = Depends(get_db)): 
    
#     posts = db.query(models.Post).all()             #This without the .all() is just a SQL query
#     return posts
    
#GET (ALL POSTS)

@app.get("/user", response_model= List[schemas.PostResponse])   #We have to import something to specify a list of posts
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()  
    return posts

#GET (SPECIFIC ID)

@app.get("/{id}", response_model= schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    test_post = db.query(models.Post).filter(models.Post.id == id).first()
    print(test_post.content)
    
    if not test_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} was not found")
    return test_post

#POST

# @app.post("/", status_code= status.HTTP_201_CREATED)
# def create_post(post: CreatePost, db: Session = Depends(get_db)):
#     new_post = models.Post(title = post.title, content = post.content, published = post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"data": new_post}

#POST (UNPACKING THE DICTIONARY)
#If we add new fields in models.Post, this method automatically unpack it for us and we don't need to always do post.title, post.content, etc.

@app.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    #Here new_post is a SQLalchemy model 
    
    #pydantic only knows how to work with dictionaries
    
    return new_post

#DELETE

@app.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post_query)
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    post_query.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)

#UPDATE

@app.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, another_post: schemas.UpdatePost, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    post_query.update(another_post.model_dump(), synchronize_session= False)
    db.commit()
    
    return post_query.first()
        
############################################## GET COMMAND ###########################################################

# @app.get("/")
# def read_root():
#     return {"Hello": "World, Okay so now it's been updated!!!"}

# @app.get("/posts/user")
# def get_posts():
#     return my_posts

#Retrieving one individual post (Without HTTPException)

# @app.get("/posts/{id}")
# def get_posts(id: int, responses: Response):     #It validated whether it can be converted to an interger, and automatically converts it
#     post = find_post(id)
#     if not post:
#         responses.status_code = status.HTTP_404_NOT_FOUND
#         return {"message" : f"Post with id : {id} was not found"}
#     return post

#Using HTTP Exceptions

# @app.get("/posts/{id}")
# def get_posts(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail= f"Post with id : {id} was not found")
#     return post

#NOW WITH DATABASE (RAW SQL)

# @app.get("/posts/user")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return posts

#Retrieving one individual post (With HTTPException)

# @app.get("/posts/{id}")
# def get_posts(id: int):     #It validated whether it can be converted to an interger, and automatically converts it
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
#     test_post = cursor.fetchone()
    
#     if not test_post:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id : {id} was not found")
#     return test_post

############################################### POST COMMAND #####################################################

# @app.post("/create_post")
# def create(payload: dict = Body(...)):  #Here, the word payload is a variable
#     print(payload)
#     return{"newpost" : f"The post has caption : {payload['text']}", "contains" : f"{payload['content']}"}

#IMPORTANT!
#pydantic : Basically what we want for the POST request
#constraint : title str, content str    (We don't want anything else)

# @app.post("/posts")
# def create(random_post : CreatePost):  #Here, the word random_post is a variable and a pydantic model
#     print(random_post.rating)
#     print(random_post.model_dump())     #Converts a pydantic model into a dictionary
# #    return{"data": "Some new post"}
#     return random_post

#Now we are going to see whether the my_post can be appended with and entry from the frontEnd

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_posts(random_post: CreatePost):
#     post_dict = random_post.model_dump()
#     post_dict['id'] = randrange(0, 100000000)
#     my_posts.append(post_dict)
#     return post_dict

#NOW WITH DATABASE (RAW SQL)

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_posts(random_post: schemas.CreatePost):
#     #Sanitize the inputs using the %s thing
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (random_post.title, 
#                                                                                              random_post.content, random_post.published))
#     new_post = cursor.fetchone()
#     conn.commit()                       #Finalize the change
#     return new_post

############################################## DELETE COMMAND ########################################################

# @app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     #Find the index in the array that has the required ID
#     #my_posts.pop(index)
#     index = find_index_post(id)
    
#     if index == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     my_posts.pop(index)
#     return Response(status_code= status.HTTP_204_NO_CONTENT)

#NOW WITH DATABASE (RAW SQL)

# @app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
    
#     cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
#     deleted_post = cursor.fetchone()
#     print(deleted_post)
#     conn.commit()
    
#     if deleted_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     return Response(status_code= status.HTTP_204_NO_CONTENT)

############################################# UPDATE COMMAND ###################################################

# @app.put("/posts/{id}")
# def update_post(id: int, another_post: UpdatePost):
#     index = find_index_post(id)
    
#     if index == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     another_post_dict = another_post.model_dump()
#     another_post_dict['id'] = id                    #Add the id separately
#     my_posts[index] = another_post_dict
#     return another_post_dict

#NOW WITH DATABASE (RAW SQL)

# @app.put("/posts/{id}")
# def update_post(id: int, another_post: schemas.UpdatePost):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (another_post.title, 
#                                                                                      another_post.content, another_post.published, 
#                                                                                      str(id)))  #str because we need to write an SQL statement 
    
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     if updated_post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
#     return updated_post