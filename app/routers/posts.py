
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas
from typing import List, Optional
from sqlalchemy.orm import Session
from ..db import get_db
from .. import oauth2
from sqlalchemy import func

router=APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut]) 
 
def get_posts(db: Session = Depends(get_db), limit: int=10, skip: int = 0, search: Optional[str]= " "):
    '''Getting all the posts'''
  
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)   #Sending data into API
def create_post(post:schemas.PostCreate, db: Session=Depends(get_db),current_user: int= Depends(oauth2.get_current_user)):

    new_post=models.Post(owner_id=current_user.id,**post.dict()) #** is used to unpack the dict and get all values from the post MODEL
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
  
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() #Filter is like WHERE in SQL (.first is retrving one item)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID: {id} was not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    
    del_post=db.query(models.Post).filter(models.Post.id == id)
    post=del_post.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID: {id} was not found")
    
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    del_post.delete(synchronize_session=False)
    db.commit()  

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put ("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    
    up_post=db.query(models.Post).filter(models.Post.id == id)
    post1=up_post.first()

    if post1==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID: {id} was not found")

    if post1.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    up_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return  up_post.first()