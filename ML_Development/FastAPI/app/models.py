#We define now all our tables with ORM as python models

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

#This will create a table within postgres
class Post(Base):       #Extend the base model from sql alchemy, Post inherits from Base
    
    #What do we want to call this table within postgres
    # __tablename__ = "posts"
    
    # id = Column(Integer, primary_key= True, nullable= False)
    # title = Column(String, nullable = False)
    # content = Column(String, nullable = False)
    # published = Column(Boolean, server_default= 'TRUE', nullable= False)
    # created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default= text('now()'))
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable= False)
    
    owner = relationship("User")    #Creates another property for our post, when we retrieve the post, it return the owner of property
                                    #It then figures out relationship to user. It fetches the user based off of the owner id and return for us
    

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default= text('now()'))