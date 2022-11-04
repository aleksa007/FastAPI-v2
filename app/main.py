from fastapi import FastAPI
from . import models
from .db import engine
from .routers import posts, users, auth, vote
from .config import Settings


models.Base.metadata.create_all(bind=engine) #enigne from db

app = FastAPI()  #instance" of the class FastAPI 

"""
@app.get("/")  #This decorator tells FastAPI that the function below corresponds to the path / with an operation get
def root(): #Function that receives a request to the URL "/" using a GET operation
    return {"message": "Hello Aleksa"}S
"""



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

