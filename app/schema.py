from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class PostBase(BaseModel):
    """
    This class defines the schema of a post
    """
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    """
    This class defines the schema of create post request
    """
    pass


class CreateUser(BaseModel):
    """
    This class defines the schema of a create user request
    """
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    """ This class defines the schema of the response to create user request"""
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class GetUserResponse(CreateUserResponse):
    pass

class PostResponse(PostBase):
    """
    This class defines the schema of response to get post request
    """
    id:int
    created_at: datetime
    owner_id:int
    owner: GetUserResponse

    class Config:
        orm_mode = True

class PostVoteResponse(BaseModel):
    """
    This class defines the schema of response to get post request
    """
    Post:PostResponse
    likes: int =0

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """
    This class defines the schema for login request
    """
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """
    This class defines the schema for login response
    """
    id:int
    token: str

class TokenData(BaseModel):
    """
    This class defines the schema for token object as received from client
    """
    id: Optional[str]=None


class Token(BaseModel):
    """
    This class defines the schema of token sent to client
    """
    token:str
    tokenType: Optional[str]= 'Bearer'


class Vote(BaseModel):
    """
    This class defines the schema/structure of a vote request
    """
    post_id:int
    vote_cast: bool
