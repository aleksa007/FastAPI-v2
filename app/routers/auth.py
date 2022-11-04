from fastapi import APIRouter, Depends,  status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import db, models
from .. import utils 
from .. import oauth2
from fastapi.security import OAuth2PasswordRequestForm



router= APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):

    us = db.query(models.User).filter(models.User.email==user_cred.username).first()

    if not us:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_cred.password, us.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #Create token

    access_token=oauth2.create_token(data = {"user_id": us.id})


    return {"token": access_token, "token_type": "bearer"}