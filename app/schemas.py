from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint 
from app.db import Base

#Base model is basicly same thing i did in pgadmin while creating the tables, also it is easier for postman to have schemams to retrive data

#from schemas import Post  #FastAPI is a Python class that provides all the functionality for your API.


#POSTS
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    time_created=datetime
    class Config:
        orm_mode=True

class Post(PostBase):
    id: int
    
    time_created: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode=True


###USER


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

###TOKEN

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

### VOTE

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

