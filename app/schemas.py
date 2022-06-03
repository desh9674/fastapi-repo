from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# this is request, something that user has to provide
class PostBase(BaseModel): # this is a Pydantic model, not the ORM model in models file
    title: str # this model is used to define user input data structure
    content: str # the ORM model is used to define db structure
    published: bool = False # true is default value, True is used always unless given specifically false
    
    #rating: Optional[int] = None # default value used if not Given

#Use of inheritance
class PostCreate(PostBase):
    pass

class PostUpdate(PostCreate):
    pass




class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True
        
# this is for response object
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # this is so that response object is a dictionary and not a pydantic model
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post: Post
    votes: int



class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)