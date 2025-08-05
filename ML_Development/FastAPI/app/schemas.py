from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# Note: Removed unused 'from re import S' since it wasn't being used

class CreatePost(BaseModel):
    """
    Schema for creating a new post.
    Used for request payload validation when creating posts.
    
    Fields:
        title (str): The title of the post (required)
        content (str): The main content of the post (required)
        published (bool): Whether the post is published (default: True)
    """
    title: str
    content: str
    published: bool = True

class UserCreateResponse(BaseModel):
    """
    Schema for user data returned in responses.
    Never includes sensitive information like passwords.
    
    Fields:
        email (EmailStr): Validated email address
        id (int): Unique user identifier
        created_at (datetime): When the user was created
    """
    email: EmailStr
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)  # Enables ORM mode for SQLAlchemy compatibility

class UpdatePost(BaseModel):
    """
    Schema for updating existing posts.
    All fields are optional in practice (PATCH operations).
    
    Fields:
        title (str): Updated title
        content (str): Updated content
        published (bool): Updated publication status
    """
    title: str
    content: str
    published: bool = True

class PostResponse(BaseModel):
    """
    Complete post data returned in responses, including owner information.
    
    Fields:
        id (int): Unique post identifier
        title (str): Post title
        content (str): Post content
        published (bool): Publication status
        created_at (datetime): When post was created
        owner_id (int): ID of the user who created the post
        owner (UserCreateResponse): Nested user information
    """
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserCreateResponse
    model_config = ConfigDict(from_attributes=True)  # Allows conversion from ORM objects

class UserWithPostCountResponse(BaseModel):
    """
    Extended user information including post count.
    Typically used for analytics or user profile endpoints.
    
    Fields:
        id (int): User ID
        email (EmailStr): User's email address
        post_count (int): Total number of posts by this user
    """
    id: int
    email: EmailStr
    post_count: int
    model_config = ConfigDict(from_attributes=True)  # Enables ORM compatibility

class UserCreate(BaseModel):
    """
    Schema for user registration (creating new users).
    
    Fields:
        email (EmailStr): Valid email address
        password (str): Plaintext password (will be hashed)
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Schema for user login credentials.
    
    Fields:
        email (EmailStr): User's registered email
        password (str): User's password
    """
    email: EmailStr
    password: str

class Token(BaseModel):
    """
    Schema for JWT token responses.
    
    Fields:
        access_token (str): The JWT token string
        token_type (str): Typically "bearer"
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for data embedded in JWT tokens.
    
    Fields:
        id (Optional[int]): User ID extracted from token
    """
    id: Optional[int] = None