from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# Base model for creating a post.
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True

# Response model for user details.
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    
    created_at: datetime

    class Config:
        from_attributes = True

class CreatePost(PostBase):
    pass


# Model for user login credentials.
class UserLogin(BaseModel):
    
    email: EmailStr
    password: str

# Response model for post details.
class PostResponse(PostBase):

    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

#  Model for post details with additional attributes.
class PostOut(BaseModel):

    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True

# Model for creating a user.
class CreateUser(BaseModel):

    email: EmailStr
    first_name: str
    last_name: str
    password: str

# Model for JWT token.
class Token(BaseModel):

    access_token: str
    token_type: str

# Model for token data.
class TokenData(BaseModel):

    id: int
    first_name: str
    last_name: str
    user_email: str


class UserUpdateResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    
    created_at: datetime

    access_token: str
    class Config:
        from_attributes = True

class VoteResponse(BaseModel):
    message: str
    likes: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class VoteUser(BaseModel):
    postid: int
